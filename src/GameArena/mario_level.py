from src.GameArena.level_map_handler import LevelMapHandler
from src.GameArena.map_camera import MapCamera
from src.GameEngine.interface import Interface
from src.util.constants import *
from pygame.locals import *


class MarioLevel(Interface):

    def __init__(self):

        super().__init__()

        self.current_level = 1

        self.map_handler = LevelMapHandler()

        self.camera = MapCamera(8,0) #NOTE: Camera Size is predefined to be the screen size
        self.camera.set_maphandler(self.map_handler)

    def start(self):

        self.map_handler.load(1)
        self.camera.init()
        #self.camera.move(self.camera.get_defaultpos())

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
        #self.map_handler.draw(self.camera,screen)
        self.camera.draw(screen)

    def update_draw(self, screen):
        #print("A")
        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)



