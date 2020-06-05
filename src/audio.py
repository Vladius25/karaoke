import pygame


class Audio:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        clock.tick(300)

    def play(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
