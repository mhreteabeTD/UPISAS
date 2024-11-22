from UPISAS.strategy import Strategy

class BaselineSpiralStrategy(Strategy):
    
    def __init__(self, exemplar):
        super().__init__(exemplar)
        self.spiral_step = [0, 0, 0]   # current step count
        self.direction = [2, 1, 0]     # initial directions
        self.original_step = [8, 8, 8] # steps to move in original direction
        self.right_step = [2, 2, 2]    # steps to move after turning right
        self.next_turn = ["return", "return", "return"] # Next action

    def analyze(self):
        """
        Analyzes the current state of the simulation.
        Fetches the monitored data using the `monitor` API.
        """
        # Fetch current monitored data
        self.monitor(with_validation=True, verbose=True)
        # Update knowledge with dynamic values (e.g., UAV positions)
        self.knowledge.dynamic_values = self.knowledge.monitored_data.get("dynamicValues", {})
        # print("Analyzed Knowledge:", self.knowledge.dynamic_values)
        return True


    def plan(self):
        uav_id = [2500, 2501, 2502]
        uav_details = []

        for i in range(3): 
            uav_details.append({"id": uav_id[i], "direction": self.direction[i]})

            self.spiral_step[i] += 1

            if self.next_turn[i] == "right":
                if self.spiral_step[i] >= self.right_step[i]:
                    # reset step counter and turn right
                    self.spiral_step[i] = 0
                    self.direction[i] = (self.direction[i] + 1) % 4
                    # increase right turn steps
                    self.right_step[i] += 2
                    if self.original_step[i] > 0:
                        self.next_turn[i] = "return"
                    else:
                        self.next_turn[i] = "right"

            elif self.next_turn[i] == "return":
                if self.spiral_step[i] >= self.original_step[i]:
                    # reset step counter and turn left back
                    self.spiral_step[i] = 0
                    self.direction[i] = (self.direction[i] - 1) % 4
                    # decrease original steps
                    self.original_step[i] = max(self.original_step[i] - 2, 0)
                    self.next_turn[i] = "right"

        self.knowledge.plan_data = {"uavDetails": uav_details}
        return True
    def execute(self):
        """
        Executes the planned directions by sending a PUT request to the API.
        """
        # Call the parent class's execute method to send the payload
        super().execute(with_validation=False)
        import json
        print("Executed with payload:", json.dumps(self.knowledge.plan_data))
