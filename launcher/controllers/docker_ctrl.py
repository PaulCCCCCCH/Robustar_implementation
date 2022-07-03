import docker

from PySide2.QtCore import QObject

class DockerController(QObject):
    def __init__(self):
        super().__init__()

        # Initialize the client to communicate with the Docker daemon
        self.client = docker.from_env()