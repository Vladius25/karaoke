import re

import mido

from src.processor import get_ticks_before_lyrics, get_syllable, get_ticks


class Parser:
    def __init__(self, file):
        self.file = file
        self.syllables = []
        self.delta_times = []

    def parse(self):
        self.process()
        self.remove_comments()
        words_with_timings = self.make_words()
        return self.make_sentences(words_with_timings)

    def process(self):
        tempo = 500000
        with open(self.file, "rb") as f:
            f.seek(13)
            data = f.read(1)
            ticks_per_beat = int.from_bytes(data, "big")
            ticks = get_ticks_before_lyrics(f.name)
            while data != b'':
                data = f.read(1)
                if data != b'\xFF':
                    continue
                data = f.read(1)
                if data == b'\x01':
                    self.syllables.append(get_syllable(f))
                    self.delta_times.append(tempo * ticks / ticks_per_beat / 1000000)
                    ticks = get_ticks(f)
                elif data == b'\x51' and f.read(1) == b'\x03':
                    tempo = int.from_bytes(f.read(3), "big")

    def remove_comments(self):
        count = 0
        while True:
            if not self.syllables[0].startswith('@'):
                break
            self.syllables.pop(0)
            count += 1
        delta = 0
        for i in range(count):
            delta += self.delta_times.pop(0)
        self.delta_times[0] += delta

    def make_words(self):
        data = list(zip(self.syllables, self.delta_times))
        word, time, result = "", 0, []
        for i, pair in enumerate(data):
            word += pair[0]
            time += pair[1]
            if pair[0].endswith(' ') or i < len(data) - 1 and data[i + 1][0].startswith(("\\", "/")):
                result.append((word, time))
                word, time = "", 0
        return result

    def make_sentences(self, words_with_timings):
        sentence, time, result = [], 0, []
        for pair in words_with_timings:
            if pair[0].startswith(("\\", "/")):
                result.append((sentence, time))
                sentence, time = [], 0
            sentence.append((re.sub(r'[\\/]', '', pair[0].strip()), pair[1]))
            time += pair[1]
        return result[1:]
