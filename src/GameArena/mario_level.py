import  pygame
from pygame.locals import *

from src.GameArena.player_mario import PlayerMario
from src.GameEngine.level_map_handler import MapHandler
from os.path import join

from src.GameEngine.interface import Interface
from src.GameEngine.map_camera import MapCamera
from src.util.constants import *


class MarioLevel(Interface):

    def __init__(self):

        super().__init__()

        self.current_level = 1
        self.map_handler = MapHandler()

        self.camera = MapCamera(0,TILE_SIZE/2,SCREEN_SIZE.width,SCREEN_SIZE.height) #NOTE: Camera Size is predefined to be the screen size
        self.camera.set_maphandler(self.map_handler)

        self.players = pygame.sprite.RenderPlain()
        self.players.add(PlayerMario(32,29*TILE_SIZE - TILE_SIZE/2))

    def start(self):

        self.map_handler.load_map(join('media', 'levels', 'level{}.txt'.format(self.current_level)))
        self.map_handler.load_tileset(join('media', 'sprites', 'tiles-level{}.bmp'.format(self.current_level)))
        self.camera.init()

    def update(self, keys):

        self.players.update(keys)

    def draw(self, screen):

        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)

    def update_draw(self, screen):
        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)
        self.players.draw(screen)



