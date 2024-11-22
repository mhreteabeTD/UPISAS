from UPISAS.exemplar import Exemplar
import random
import os
import subprocess
import logging
class WildfireUAVExemplar(Exemplar):
    """
    A class which encapsulates the Wildfire-UAVSim exemplar run in a Docker container.
#     """
#     def __init__(self, auto_start=False, container_name="wildfire-container4"):
#         """
#         Initialize the Wildfire-UAVSim exemplar.
#         """
#         docker_config = {
#             "name": container_name ,  # Name of the container
#             # "image": "mhreteabe/wildfire-uav",  # Docker image built from the provided Dockerfile,
#             "image": "wildfire-uvasim-image",  # Docker image built from the provided Dockerfile
#             "ports": {"8521/tcp": 8521, "55555/tcp": 55555},    # Port mappings
#             "volumes": {"/.": {"bind": "/code", "mode": "rw"}  # Mount current directory to /code in the container},}
# }
#             }

#         # Initialize the parent class with the API endpoint and Docker config
#         super().__init__("http://localhost:55555", docker_config, auto_start)
#         print(
#             "WildfireUAVExemplar initialized. API endpoint: http://localhost:55555"
#         )
    def __init__(self, auto_start=True, container_name = "wildfire-container"):
        self.base_endpoint = "http://localhost:55555"
        self.wildfire_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "Wildfire-UAVSim")) #absolute path used to avoid issues when running the script from different locations

        if auto_start:
            self.start_container()

    # def start_run(self):
    #     """
    #     Start the Wildfire-UAVSim API service inside the container.
    #     """
    #     self.exemplar_container.exec_run(
    #         # cmd = f' sh -c "" '
    #         cmd="python3 /code/wildfire/api.py",  # Command to run the API
    #         detach=True  # Run the process in detached mode
    #     )
    def start_run(self):
        # try:
        #     subprocess.run( ['', 'wildfire/api.py'], cwd = self.wildfire_dir_path, check = True )
        #     logging.info ("Docker container is now started and running successfully...")
        # except subprocess.CalledProcessError as e:
        #     logging.error(f"Failed to start the docker containers: {e}")
        #     raise
        pass

    def start_container(self):
        try:
            subprocess.Popen( ['make', 'runFirst'], cwd = self.wildfire_dir_path)
            logging.info ("Docker container is now started and running successfully...")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to start the docker containers: {e}")
            raise

    def stop_container(self, remove=True):
        try:
            subprocess.run(
                ['make', 'stop'],
                cwd = self.wildfire_dir_path,
                check=True
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to stop the docker containers: {e}")
            raise
