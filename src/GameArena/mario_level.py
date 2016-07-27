from os.path import join

from src.GameArena.level_map_handler import MapHandler
from src.GameArena.map_camera import MapCamera
from src.GameEngine.interface import Interface
from src.util.constants import *
from pygame.locals import *


class MarioLevel(Interface):

    def __init__(self):

        super().__init__()

        self.current_level = 1
        self.map_handler = MapHandler()

        self.camera = MapCamera(0,0,SCREEN_SIZE.width,SCREEN_SIZE.height) #NOTE: Camera Size is predefined to be the screen size
        self.camera.set_maphandler(self.map_handler)

    def start(self):

        self.map_handler.load_map(join('media', 'levels', 'level{}.txt'.format(self.current_level)))
        self.map_handler.load_tileset(join('media', 'sprites', 'tiles-level{}.bmp'.format(self.current_level)))
        self.camera.init()

    def update(self, keys):

        if keys[K_RIGHT]:
            self.camera.move(1, 0)

        if keys[K_LEFT]:
            self.camera.move(-1, 0)

        if keys[K_UP]:
            self.camera.move(0, -1)

        if keys[K_DOWN]:
            self.camera.move(0, 1)

    def draw(self, screen):

        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)

    def update_draw(self, screen):
        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)



