import pygame
from pygame.locals import *


def init_pygame():
    pygame.init()


class GameManager:
    def __init__(self, caption, size=(320, 240), fps=100):
        self.quit = False
        self.interfaces = []
        self.size = size
        self.fps = fps
        self.caption = caption

        init_pygame()
        self.set_mode()
        self.clock = pygame.time.Clock()

    def set_mode(self):
        self.screen = pygame.display.set_mode(self.size)
        self.rect_screen = self.screen.get_rect()
        pygame.display.set_caption(self.caption)

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

    def run(self):

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
            self.clock.tick(self.fps)
