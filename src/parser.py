import re

import mido

from src.processor import get_ticks_before_lyrics, get_syllable, get_ticks


class Parser:
    """
    Класс для парсинга midi файла
    """

    def __init__(self, file):
        self.file = file
        self.syllables = []
        self.delta_times = []

    def parse(self):
        """
        Разбивает файл на слова с таймингами и предлодения
        :return: [[(str, int), (str, int)], ...], [str, str, str]
        """
        self.process()
        self.remove_comments()
        words_with_timings = self.split_words_by_sentences(
            self.make_words_with_timings()
        )
        return words_with_timings, self.make_sentences(words_with_timings)

    def process(self):
        """
        Обрабатывает мета ивенты
        """
        tempo = 500000
        with open(self.file, "rb") as f:
            f.seek(13)
            data = f.read(1)
            ticks_per_beat = int.from_bytes(data, "big")
            ticks = get_ticks_before_lyrics(f.name)
            while data != b"":
                data = f.read(1)
                if data != b"\xFF":
                    continue
                data = f.read(1)
                if data == b"\x01":
                    self.syllables.append(get_syllable(f))
                    self.delta_times.append(tempo * ticks / ticks_per_beat / 1000000)
                    ticks = get_ticks(f)
                elif data == b"\x51" and f.read(1) == b"\x03":
                    tempo = int.from_bytes(f.read(3), "big")

    def remove_comments(self):
        """
        Удаляет строчки, не относящиеся к содержанию
        """
        count = 0
        while True:
            if not self.syllables[0].startswith("@"):
                break
            self.syllables.pop(0)
            count += 1
        delta = 0
        for i in range(count):
            delta += self.delta_times.pop(0)
        self.delta_times[0] += delta

    def make_words_with_timings(self):
        """
        Преобразует слоги в слова с таймингами
        :return: [(str, int), (str, int), ...]
        """
        data = list(zip(self.syllables, self.delta_times))
        word, time, result = "", 0, []
        for i, pair in enumerate(data):
            word += pair[0]
            time += pair[1]
            if (
                pair[0].endswith(" ")
                or i < len(data) - 1
                and data[i + 1][0].startswith(("\\", "/"))
            ):
                result.append((word, time))
                word, time = "", 0
        return result

    def split_words_by_sentences(self, words_with_timings):
        """
        Группиурет слова по предложениям
        :param words_with_timings:
        :return: [[(str, int), (str, int)], ...]
        """
        result, sentence = [], []
        for word, timing in words_with_timings:
            if word.startswith(("\\", "/")):
                result.append(sentence)
                sentence = []
            sentence.append((re.sub(r"[\\/]", "", word.strip()), timing))
        result.append(sentence)
        return result[1:]

    def make_sentences(self, words_with_timings):
        """
        Делает из слов предложения
        :param words_with_timings: уже разделенные на предложения
        :return: [str, str, str, ...]
        """
        sentences = []
        for sentence in words_with_timings:
            res = ""
            for word, _ in sentence:
                res += word + " "
            sentences.append(res)
        return sentences
