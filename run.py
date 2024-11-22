from UPISAS.strategies.swim_reactive_strategy import ReactiveAdaptationManager
from UPISAS.strategies.random_UAV_movement import RandomUAVStrategy
from UPISAS.exemplar import Exemplar
from UPISAS.exemplars.swim import SWIM
from UPISAS.exemplars.Wildfire import WildfireUAVExemplar
import signal
import sys
import time

if __name__ == '__main__':
    
    exemplar = WildfireUAVExemplar(auto_start=True)
    time.sleep(10)
    exemplar.start_run()
    time.sleep(3)

    try:
        strategy = RandomUAVStrategy(exemplar)
        strategy.get_monitor_schema()
        strategy.get_adaptation_options_schema()
        strategy.get_execute_schema()

        while True:
            time.sleep(5)
            # input("Try to adapt?")
            strategy.monitor(verbose=False)
            if strategy.analyze():
                if strategy.plan():
                    strategy.execute()
            
    except (Exception, KeyboardInterrupt) as e:
        print(str(e))
        input("something went wrong")
        exemplar.stop_container()
        sys.exit(0)