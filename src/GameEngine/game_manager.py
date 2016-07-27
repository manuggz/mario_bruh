import pygame

from src.util.constants import *
from src.util.constants import FPS_GAME


def init_pygame():
    pygame.init()


class GameManager:
    def __init__(self, caption):
        self.quit = False
        self.screen = None
        self.interfaces = []

        init_pygame()
        self.set_mode()
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def set_mode(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size)
        self.rect_screen = self.screen.get_rect()

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
                elif event.type == KEYDOWN:
                    if event.key == K_F5:
                        pygame.display.toggle_fullscreen()
                    elif event.key == K_q:
                        self.quit = True

            if self.has_interface():
                self.interfaces[-1].update(pygame.key.get_pressed())
                self.interfaces[-1].update_draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS_GAME)

    def run(self):
        self.__main_loop()
