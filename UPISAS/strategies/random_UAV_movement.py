import random
from UPISAS.strategy import Strategy


class RandomUAVStrategy(Strategy):
    """
    A random strategy for UAVs that moves them in random directions at each step.
    """

    def analyze(self):
        """
        Analyzes the current state of the simulation.
        Fetches the monitored data using the `monitor` API.
        """
        # Fetch current monitored data
        self.monitor(with_validation=True, verbose=True)
        # Update knowledge with dynamic values (e.g., UAV positions)
        self.knowledge.dynamic_values = self.knowledge.monitored_data.get("dynamicValues", {})
        print("Analyzed Knowledge:", self.knowledge.dynamic_values)
        return True

    def plan(self):
        """
        Plans a random set of movements for the UAVs.
        Updates the `plan_data` in knowledge.
        """
        # Extract UAV details from the monitored data
        uav_details = self.knowledge.dynamic_values[0].get("uavDetails", [])

        # Generate random directions for each UAV
        # possible_dirs = ['left', 'right', 'up', 'down']
        directions = [
            {"id": uav["id"], "direction":random.randint(0, 3)}  # 0-3 correspond to [north, south, east, west]
            for uav in uav_details
        ]
        print("Planned Directions:", directions)

        # Update knowledge plan data with the generated directions
        self.knowledge.plan_data = {"uavDetails": directions}
        return True
    def execute(self):
        """
        Executes the planned directions by sending a PUT request to the API.
        """
        # Call the parent class's execute method to send the payload
        super().execute(with_validation=False)
        import json
        print("Executed with payload:", json.dumps(self.knowledge.plan_data))
