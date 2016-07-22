import pygame
from pygame.locals import *


def init_pygame():
    pygame.init()


class GameManager:

    def __init__(self):
        self.quit = False
        self.screen = None
        self.size_screen = Rect(0, 0, 640, 480)
        self.interfaces = []

        init_pygame()
        self.set_mode()

    def set_mode(self):
        self.screen = pygame.display.set_mode(self.size_screen.size)

    def push_interface(self, nueva_interface):

        if nueva_interface:

            nueva_interface.start()
            nueva_interface.draw(self.screen)

            self.interfaces.append(nueva_interface)

    def pop_interface(self):
        try:
            return self.interfaces.pop()
        except IndexError:
            return None

    def has_interface(self):

        return len(self.interfaces)

    def __main_loop(self):

        while not self.quit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit = True

            if self.has_interface():
                self.interfaces[-1].update()
                self.interfaces[-1].update_draw(self.screen)

            pygame.display.flip()

    def run(self):
        self.__main_loop()
