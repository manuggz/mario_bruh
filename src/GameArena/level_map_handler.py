from os.path import join
import pygame
from src.util.constants import *


def normalize(n, unit):
    return (n // unit) * unit


def create_camera_rect(rect_camera_visible):

    rect_camera_map = rect_camera_visible.copy()
    rect_camera_map.x = normalize(rect_camera_visible.x, TILE_SIZE)
    rect_camera_map.y = normalize(rect_camera_visible.y, TILE_SIZE)

    rect_camera_map.width = normalize(rect_camera_visible.right, TILE_SIZE) - rect_camera_map.x
    if rect_camera_visible.right > rect_camera_map.right:
        rect_camera_map.width += TILE_SIZE

    rect_camera_map.height = normalize(rect_camera_visible.bottom, TILE_SIZE) - rect_camera_map.y
    if rect_camera_visible.bottom > rect_camera_map.bottom:
        rect_camera_map.height += TILE_SIZE

    return rect_camera_map


class LevelMapHandler:

    def __init__(self):
        self.matrix_level = None
        self.rect_map = None
        self.tiles = None

    def load(self, n_level):

        # Tile s positioning data
        file_level = open(join('media', 'levels', 'level{}.txt'.format(n_level)))

        self.matrix_level = [[int(i) for i in list(line.strip())] for line in file_level.readlines()]
        file_level.close()
        self.rect_map = Rect(0, 0, len(self.matrix_level[0]) * TILE_SIZE, len(self.matrix_level) * TILE_SIZE)
        # Tile s image
        self.tiles = pygame.image.load(join('media', 'sprites', 'tiles-level{}.bmp'.format(n_level)))

    def is_rect_out_of_map_bounds(self, rect):
        return not self.rect_map.contains(rect)

    def clamp_rect(self, rect):
        return rect.clamp(self.rect_map)

    # Create a Surface that contains/draws all the visible tiles that are contained in rect_cut
    def create_image(self, rect_camera_map):
        # pre: rect_image must be created <TILE_SIZE*rows>X<TILE_SIZE*columns>

        image_map_tile = pygame.Surface(rect_camera_map.size, SRCALPHA)

        n_rows = rect_camera_map.height // TILE_SIZE
        n_columns = rect_camera_map.width // TILE_SIZE

        i_init_matriz = rect_camera_map.y // TILE_SIZE
        j_init_matriz = rect_camera_map.x // TILE_SIZE

        src_srfc_tile_rect = Rect(0, 0, TILE_SIZE, TILE_SIZE)

        for i in range(n_rows):
            for j in range(n_columns):
                i_matrix = i_init_matriz + i
                j_matrix = j_init_matriz + j

                tile_index = self.matrix_level[i_matrix][j_matrix]

                if tile_index != BLOQUE_NIL:
                    src_srfc_tile_rect.x = TILE_SIZE * (tile_index - 1)
                    image_map_tile.blit(self.tiles, (
                    (j_matrix - j_init_matriz) * TILE_SIZE, (i_matrix - i_init_matriz) * TILE_SIZE), src_srfc_tile_rect)

        return image_map_tile
