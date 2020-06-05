import pygame


class Audio:

    def __init__(self):
        pygame.init()

    def play(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
