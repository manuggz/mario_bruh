import pygame
from os.path import join
from pygame.locals import *
from src.GameArena.states_player import StandingRight
from src.GameEngine.sprite_sheet import SpriteSheet


class PlayerMario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = SpriteSheet(join("media", "sprites", "litle_mario.png"), 2, 14)
        self.status = StandingRight(self, x, y, self.sprite_sheet)

    def update(self, keys):
        self.status.update(keys)
        self.image, self.rect = self.status.get_frame()

    def change_status(self, new_status):
        self.status = new_status
