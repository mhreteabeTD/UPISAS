from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, List, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
import time

from UPISAS.strategies.random_UAV_movement import RandomUAVStrategy
from UPISAS.exemplars.Wildfire import WildfireUAVExemplar

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name: str = "wildfire_uav_runner_experiment"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment."""
    results_output_path: Path = ROOT_DIR / 'experiments'

    """Experiment operation type."""
    operation_type: OperationType = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes."""
    time_between_runs_in_ms: int = 1000

    exemplar = None
    strategy = None

    def __init__(self):
        """Executes immediately after program start, on config load."""
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment)
        ])
        self.run_table_model = None  # Initialized later

        output.console_log("Wildfire UAV config loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here."""
        factor1 = FactorModel("uav_count", [2, 3, 5][:1])  # Vary the number of UAVs
        self.run_table_model = RunTableModel(
            factors=[factor1],
            exclude_variations=[],
            data_columns=['MR1_1','MR1_2','MR1_3' ,'MR1_AVG','MR2']  # Add metrics to track
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here."""
        output.console_log("Config.before_experiment() called!")

    def before_run(self) -> None:
        """Perform any activity required before starting a run."""
        self.exemplar = WildfireUAVExemplar(auto_start=True)
        self.strategy = RandomUAVStrategy(self.exemplar)  # Use the random strategy for this example
        time.sleep(30)
        output.console_log("Config.before_run() called!")

    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run."""
        # Set dynamic variables for this run, if necessary
        self.exemplar.start_run()
        time.sleep(3)
        output.console_log("Config.start_run() called!")

    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        output.console_log("Config.start_measurement() called!")

    def interact(self, context: RunnerContext) -> None:
        """Perform interactions with the running system."""
        time_slept = 0
        self.strategy.get_monitor_schema()
        self.strategy.get_adaptation_options_schema()
        self.strategy.get_execute_schema()

        while time_slept < 60 * 5:  # Run the strategy for 30 seconds
            self.strategy.monitor(verbose=False)
            self.strategy.analyze()
            self.strategy.plan()
            self.strategy.execute()

            time.sleep(3)
            time_slept += 3

        output.console_log("Config.interact() called!")

    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
        output.console_log("Config.stop_measurement() called!")

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run."""
        self.exemplar.stop_container()
        output.console_log("Config.stop_run() called!")

    def populate_run_data(self, context: RunnerContext) -> List[Dict[str, any]]:
        """
        Parse and process measurement data for each simulation run.
        Each item in the list contains MR1 and MR2 values for that run,
        and the function collects these along with UAV details.
        """
        # Retrieve the list of all runs, which are dictionaries containing MR1, MR2, and UAV details
        simulation_runs = self.strategy.knowledge.monitored_data['dynamicValues']

        # Initialize a list to store the results for each run
        run_results = []
        mr1_1 = []
        mr1_2 = []
        mr1_3 = []
        mr1_avg_values= []
        mr2 = []
        # Iterate over each run
        for run in simulation_runs:
            mr1_values = run.get('MR1', [])
            mr2_value = run.get('MR2', 0)
            uav_details = run.get('uavDetails', [])

            # Calculate the average MR1 for this run if there are any MR1 values
            mr1_avg = sum(mr1_values) / len(mr1_values) if mr1_values else 0

            mr1_avg_values.append(mr1_avg)
            mr1_1.append(mr1_values[0] if len(mr1_values) > 0 else 0)
            mr1_2.append(mr1_values[1] if len(mr1_values) > 1 else 0)
            mr1_3.append(mr1_values[2] if len(mr1_values) > 2 else 0)
            mr2.append(mr2_value)
            # Log each run's data
            # output.console_log(f"Run data: MR1 Average={mr1_avg}, MR2={mr2_value}, UAVs={uav_details}")

        run_data = {
            "MR1_1": mr1_1,
            "MR1_2": mr1_2,
            "MR1_3": mr1_3,
            "MR1_AVG": mr1_avg_values,
            "MR2": mr2
        }
            
        # Return the data for all runs
        return run_data


    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment."""
        output.console_log("Config.after_experiment() called!")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path: Path = None
