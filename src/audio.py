import pygame


class Audio:
    """
    Класс для воспроизведения музыки из файла
    """

    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        clock.tick(300)

    def play(self, file):
        """
        Проигрывает музыку из файла
        :param file: str
        :return:
        """
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def stop(self):
        """
        Останавливает музыку
        :return:
        """
        pygame.mixer.music.stop()
