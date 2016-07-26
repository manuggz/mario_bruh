import pygame
from pygame.locals import *

from src.GameArena.level_map_handler import LevelMapHandler
from src.util.constants import *


class MapCamera:

    def __init__(self,x_init,y_init):
        self.pos_default = (x_init,y_init)
        self.rect_visible_camera = Rect(x_init, y_init, *SCREEN_SIZE)
        self.map_handler = None

        self.map_tile_surface = None
        self.rect_map_tile_camera = None

    def init(self):
        assert self.map_handler is not None, "There's not a " + str(LevelMapHandler.__class__) + " instance "

        self.rect_map_tile_camera = self.map_handler.create_camera_rect(self.rect_visible_camera)
        self.map_tile_surface = self.map_handler.create_image(self.rect_map_tile_camera)


    def set_maphandler(self, map_handler):
        self.map_handler = map_handler

    def get_defaultpos(self):
        return self.pos_default

    def move(self,x,y):

        rect_moved = self.rect_visible_camera.move(x,y)

        if self.map_handler.is_rect_out_of_map_bounds(rect_moved): return

        self.rect_visible_camera.move_ip(x, y)

        if not self.rect_map_tile_camera.contains(self.rect_visible_camera):

            self.rect_map_tile_camera = self.map_handler.create_camera_rect(self.rect_visible_camera)
            self.map_tile_surface = self.map_handler.create_image(self.rect_map_tile_camera)


    def draw(self, screen):
        rect_area_visible = self.rect_visible_camera.copy()
        rect_area_visible.x -= self.rect_map_tile_camera.x
        rect_area_visible.y -= self.rect_map_tile_camera.y
        #print(rect_area_visible)
        screen.blit(self.map_tile_surface, (0, 0), rect_area_visible)

