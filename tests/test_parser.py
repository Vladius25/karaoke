import os
import unittest

from src.parser import Parser
from src.processor import get_syllable, get_ticks, get_ticks_before_lyrics


class ProcessorTest(unittest.TestCase):
    def setUp(self):
        with open("testing.kar", "rb") as f:
            self.parser = Parser(f)

    def test_remove_comments(self):
        self.parser.syllables.extend(["@1", "@2", "@3", "4"])
        self.parser.delta_times.extend([1, 2, 3, 4])

        self.parser.remove_comments()

        self.assertEqual(["4"], self.parser.syllables)
        self.assertEqual([10], self.parser.delta_times)

    def test_make_words_with_timings(self):
        self.parser.syllables.extend(["1", "2 ", "/3", "4 "])
        self.parser.delta_times.extend([1, 2, 3, 4])

        result = self.parser.make_words_with_timings()

        self.assertEqual([('12 ', 3), ('/34 ', 7)], result)

    def test_split_words_by_sentences(self):
        result = self.parser.split_words_by_sentences([('/12', 3), ('34 ', 7), ('/33', 8), ('22', 90)])
        self.assertEqual([[('12', 3), ('34', 7)], [('33', 8), ('22', 90)]], result)

    def test_make_sentences(self):
        result = self.parser.make_sentences([[('12', 3), ('34', 7)], [('33', 8), ('22', 90)]])
        self.assertEqual(['12 34 ', '33 22 '], result)
