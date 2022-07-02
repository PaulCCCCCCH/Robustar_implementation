import docker

from PySide2.QtCore import QObject

class DockerController(QObject):
    def __init__(self):
        super().__init__()