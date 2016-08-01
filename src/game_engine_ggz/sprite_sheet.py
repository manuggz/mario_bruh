import pygame
from pygame.locals import *


class SpriteSheet:
    def __init__(self, path, n_rows, n_cols):

        self.n_frames = n_rows * n_cols
        self.n_rows = n_rows
        self.n_cols = n_cols
        self._frames = pygame.image.load(path)

        self.rect_frame_focus = Rect(0, 0, self._frames.get_width() / n_cols, self._frames.get_height() / n_rows)

        self.frame_list = []
        for i in range(self.n_rows):
            line = []
            self.rect_frame_focus.y = i * self.rect_frame_focus.h
            for j in range(self.n_cols):
                self.rect_frame_focus.x = j * self.rect_frame_focus.w
                line.append(self._frames.subsurface(self.rect_frame_focus))

            self.frame_list.append(line)

    def get(self, row, col):
        return self.frame_list[row - 1][col - 1]

    def get_rect(self):
        rect = self.rect_frame_focus.copy()
        rect.x = 0
        rect.y = 0
        return rect
