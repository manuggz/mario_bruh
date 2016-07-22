import pygame
from pygame.locals import *
from src.util.constants import *


class MapCamera:

    def __init__(self):

        self.pos = Rect(0,0,*SCREEN_SIZE)
