import os

from src.audio import Audio
from src.parser import Parser


class State:
    def __init__(self):
        self.audio = Audio()
        self.file = None
        self.track_name = ""

    def run(self, file):
        self.file = file
        parser = Parser(file)
        self.track_name = os.path.basename(file)
        self.play(file)
        return parser.parse()

    def play(self, file):
        self.audio.play(file)

