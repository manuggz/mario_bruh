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


def get_integer_gt0(value, name_value):
    try:
        value = int(value)
        if value <= 0:
            raise Exception(name_value + " {} must be greater than zero".format(value))

        return value
    except ValueError:
        raise Exception(name_value + " {} must be an Integer".format(value))


def read_n_rows_columns_num_tiles(file_level):
    n_rows, n_cols, n_tiles = file_level.readline().strip().split(" ")
    n_rows = get_integer_gt0(n_rows, "rows")
    n_cols = get_integer_gt0(n_cols, "columns")
    n_tiles = get_integer_gt0(n_tiles, "n_tiles")
    return n_rows, n_cols, n_tiles


class MapHandler:
    def __init__(self):

        self.matrix_tiles = None
        self.rect_full_map = None
        self.tileset_surface = None

    def load(self, path_to_file_level, path_to_file_image):

        # Tile s positioning data
        file_level = open(path_to_file_level)

        self.matrix_tiles = []
        # lines = file_level.readlines()
        # n_lines = len(lines)
        n_rows, n_cols, n_tiles = read_n_rows_columns_num_tiles(file_level)

        i = 0
        while i < n_rows:
            j = 0
            line = list(file_level.readline().strip())
            while j < n_cols:
                try:
                    line[j] = int(line[j])
                    if line[j] < 0 or line[j] >= n_tiles:
                        raise Exception("Tile Value at ({0},{1}) must be in range {2}-{3}. '{4}' not permitted".
                                         format(i + 2, j + 1, 0, n_tiles - 1, line[j]))

                except ValueError:
                    raise Exception("Tile Value at ({0},{1}) must be an Integer. '{2}' not permitted".
                                     format(i + 2, j + 1, line[j]))

                j += 1

            self.matrix_tiles.append(line)
            i += 1

        file_level.close()
        self.rect_full_map = Rect(0, 0, len(self.matrix_tiles[0]) * TILE_SIZE, len(self.matrix_tiles) * TILE_SIZE)
        # Tile s image
        self.tileset_surface = pygame.image.load(path_to_file_image)


    def is_rect_out_of_map_bounds(self, rect):
        return not self.rect_full_map.contains(rect)

    def clamp_rect(self, rect):
        return rect.clamp(self.rect_full_map)

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

                tile_index = self.matrix_tiles[i_matrix][j_matrix]

                if tile_index != BLOQUE_NIL:
                    src_srfc_tile_rect.x = TILE_SIZE * (tile_index - 1)
                    image_map_tile.blit(self.tileset_surface, (
                        (j_matrix - j_init_matriz) * TILE_SIZE, (i_matrix - i_init_matriz) * TILE_SIZE),
                                        src_srfc_tile_rect)

        return image_map_tile
