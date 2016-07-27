from pygame.locals import *
from .interface import Interface


class ColorInterface(Interface):

    def __init__(self, parent,color_name):
        super().__init__(parent)
        self.color = color.THECOLORS[color_name]

    def draw(self, screen):
        screen.fill(self.color)
