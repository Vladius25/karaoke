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

    def run(self):
        """
        Запускает парсер и музыку
        """
        parser = Parser(self.file)
        self.track_name = os.path.basename(self.file)
        self.play(self.file)
        self.words_with_timings, self.sentences = parser.parse()

    def play(self, file):
        """
        Проигрывает музыку
        :param file: str
        """
        self.audio.play(file)

    def stop(self):
        """
        Останавлиает музыку
        """
        self.audio.stop()
