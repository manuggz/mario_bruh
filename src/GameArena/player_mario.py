from os.path import join

import pygame
from src.game_engine_ggz.sprite_sheet import SpriteSheet

from src.GameArena.states_player import StandingRight


class PlayerMario(pygame.sprite.Sprite):
    def __init__(self, interface, x, y):
        super().__init__()
        self.stage = interface

        self.x, self.y = x, y
        self.jump_power = -5.7
        self.move_speed = 1
        self.jump_pressed = False
        self.sprite_sheet = SpriteSheet(join("media", "sprites", "litle_mario.png"), 2, 14)
        self.state = StandingRight(self)
        self.image = self.sprite_sheet.get(*self.state.animation.get_current_frame())
        self.rect = self.sprite_sheet.get_rect()
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h

    def update(self, keys):
        self.state.update(keys)
        self.image = self.sprite_sheet.get(*self.state.animation.get_current_frame())

    def has_solid_bottom(self):
        return self.stage.has_solid_bottom(self.rect.copy())

    def move(self, x_add, y_add):
        self.x += x_add
        self.y += y_add

        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h

    def change_state(self, new_status):
        self.state = new_status

    def is_out_of_screen_bounds(self):
        return self.stage.is_out_of_screen_bounds(self.rect.copy())

    def collide_map(self):
        return self.stage.collide_map(self.rect.copy())

    def get_floor_dist(self, max_dist):
        """Obtiene la distancia entre el punto (x, y) y el proximo bloque solido hacia abajo"""
        return self.stage.get_floor_dist(self.x, self.y, max_dist)
