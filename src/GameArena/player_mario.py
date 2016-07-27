import pygame
from os.path import join
from pygame.locals import *
from src.GameArena.states_player import StandingRight
from src.GameEngine.sprite_sheet import SpriteSheet


class PlayerMario(pygame.sprite.Sprite):
    def __init__(self, parent, x, y):
        super().__init__()

        self.sprite_sheet = SpriteSheet(join("media", "sprites", "litle_mario.png"), 2, 14)
        self.state = StandingRight(self, x, y, self.sprite_sheet)
        self.parent = parent

    def update(self, keys):
        self.state.update(keys)
        self.image, self.rect = self.state.get_image(), self.state.get_rect()

    def change_status(self, new_status):
        self.state = new_status

    def is_out_of_screen_bounds(self, rect):
        return self.parent.is_out_of_screen_bounds(rect)

    def collide_map(self,rect):
        return self.parent.collide_map(rect)