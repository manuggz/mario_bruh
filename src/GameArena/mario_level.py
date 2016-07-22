from src.GameArena.level_map_handler import LevelMapHandler
from src.GameEngine.interface import Interface
from src.util.constants import *
from pygame.locals import *


class MarioLevel(Interface):

    def __init__(self):

        super().__init__()

        self.current_level = 1
        self.map_handler = LevelMapHandler()

    def start(self):

        self.map_handler.load(1)

    def draw(self, screen):

        screen.fill(FONDO_LIGHTBLUE)

