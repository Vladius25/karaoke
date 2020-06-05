import os

from src.audio import Audio
from src.parser import Parser


class State:
    def __init__(self):
        self.audio = Audio()
        self.file = None
        self.track_name = ""
        self.words_with_timings = []
        self.sentences = []

    def run(self, file):
        """
        Запускает парсер и музыку
        :param file: путь до .kar файла
        """
        self.file = file
        parser = Parser(file)
        self.track_name = os.path.basename(file)
        self.play(file)
        self.words_with_timings, self.sentences = parser.parse()

    def play(self, file):
        self.audio.play(file)

    def stop(self):
        self.audio.stop()
