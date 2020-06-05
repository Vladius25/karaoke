import os
import unittest

from src.processor import get_syllable, get_ticks, get_ticks_before_lyrics


class ProcessorTest(unittest.TestCase):
    def tearDown(self):
        if os.path.exists("file.txt"):
            os.remove("file.txt")

    def test_get_ticks_before_lyrics(self):
        ticks = get_ticks_before_lyrics("testing.kar")
        self.assertEqual(24, ticks)

    def test_get_syllable(self):
        with open("file.txt", "wb") as f:
            f.write(b"\x02\xFF\x58\x67")
        with open("file.txt", "rb") as f:
            syl = get_syllable(f)
            self.assertEqual('яX', syl)

    def test_get_ticks(self):
        with open("file.txt", "wb") as f:
            f.write(b"\x82\x08\xFF\x01")
        with open("file.txt", "rb") as f:
            num = get_ticks(f)
            self.assertEqual(264, num)
