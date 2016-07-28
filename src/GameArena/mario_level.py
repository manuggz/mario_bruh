import pygame
from pygame.locals import *

from src.GameArena.player_mario import PlayerMario
from src.GameEngine.level_map_handler import MapHandler
from os.path import join

from src.GameEngine.interface import Interface
from src.GameEngine.map_camera import MapCamera
from src.util.constants import *


class MarioLevel(Interface):
    def __init__(self, parent):
        super().__init__(parent)

        self.current_level = 1
        self.map_handler = MapHandler()

        self.camera = MapCamera(0, 0, SCREEN_SIZE.width,SCREEN_SIZE.height)  # NOTE: Camera Size is predefined to be the screen size
        self.camera.set_maphandler(self.map_handler)

        self.players = pygame.sprite.RenderPlain()
        self.player1 = PlayerMario(self, 32, 13 * TILE_SIZE)
        self.players.add(self.player1)

        self.camera.follow(self.player1)

    def start(self):
        self.map_handler.load_map(join('media', 'levels', 'level{}.txt'.format(self.current_level)))
        self.map_handler.load_tileset(join('media', 'sprites', 'tiles-level{}.bmp'.format(self.current_level)))
        self.camera.init()

    def is_out_of_screen_bounds(self, rect):
        return self.map_handler.is_rect_out_of_map_bounds(rect) or self.camera.is_rect_out_of_camera_bounds(rect)

    def collide_map(self, rect):
        return self.map_handler.collide_map(rect)

    def get_floor_dist(self, x, y, max_dist):
        "Obtiene la distancia entre el punto (x, y) y el proximo bloque solido hacia abajo"
        return self.map_handler.get_floor_dist(x, y , max_dist)

    def has_solid_bottom(self, rect):
        nearest = self.map_handler.get_nearest_bottom_tile(rect, 1)
        return nearest and nearest[2] == 0

    def update(self, keys):
        self.players.update(keys)
        self.camera.update()

    def draw(self, screen):
        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)

    def update_draw(self, screen):
        screen.fill(FONDO_LIGHTBLUE)
        self.camera.draw(screen)

        for player in self.players:
            rect = player.rect.copy()
            rect.x -= self.camera.get_x()
            rect.y -= self.camera.get_y()
            screen.blit(player.image,rect)
