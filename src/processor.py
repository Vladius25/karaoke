import os

import mido
from bitstring import BitArray


def get_ticks_before_lyrics(file):
    mid = mido.MidiFile(file)
    for track in mid.tracks[2]:
        ticks = str(track).find("text")
        if ticks > 0:
            return ticks


def get_syllable(file):
    length = int.from_bytes(file.read(1), "big")
    return file.read(length).decode("cp1251")


def get_ticks(file):
    delta_time = ""
    while True:
        data = BitArray(file.read(1)).bin
        delta_time += data[1:]
        if data[0] == '0':
            break
    file.seek(-1, os.SEEK_CUR)
    return int(delta_time, 2)
