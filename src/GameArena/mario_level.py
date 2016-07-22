from pygame.locals import *
from src.GameEngine.interface import Interface
from src.util.constants import *

class MarioLevel(Interface):

    def draw(self, screen):
        screen.fill(FONDO_LIGHTBLUE)