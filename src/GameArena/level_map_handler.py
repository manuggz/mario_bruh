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
            raise AssertionError(name_value + " {} must be greater than zero".format(value))

        return value
    except ValueError:
        raise AssertionError(name_value + " {} must be an Integer".format(value))


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
        self.is_map_loaded = False
        self.n_rows = 0
        self.n_cols = 0
        self.n_tiles = 0
        self.path_to_tileset = None

    # Load a file containing tile positioning
    def load_map(self, path_to_file_level):

        # Tile s positioning data
        file_level = open(path_to_file_level)

        self.matrix_tiles = []
        # lines = file_level.readlines()
        # n_lines = len(lines)
        self.n_rows, self.n_cols, self.n_tiles = read_n_rows_columns_num_tiles(file_level)

        if self.is_map_loaded: self.check_loaded_tileset()  # We check that we can cover the tiles with our current
        #tile set

        i = 0
        while i < self.n_rows:
            j = 0
            line = list(file_level.readline().strip())
            while j < self.n_cols:
                try:
                    line[j] = int(line[j])
                    if line[j] < 0 or line[j] >= self.n_tiles:
                        raise AssertionError("Tile Value at ({0},{1}) must be in range {2}-{3}. '{4}' not permitted".
                                             format(i + 2, j + 1, 0, self.n_tiles - 1, line[j]))

                except ValueError:
                    raise AssertionError("Tile Value at ({0},{1}) must be an Integer. '{2}' not permitted".
                                         format(i + 2, j + 1, line[j]))
                except IndexError:
                    raise AssertionError("Wrong number of tiles at line {0}. {1} tiles are missing".
                                         format(i + 2, self.n_cols - j))

                j += 1

            self.matrix_tiles.append(line)
            i += 1

        file_level.close()
        self.rect_full_map = Rect(0, 0, self.n_cols * TILE_SIZE, self.n_rows * TILE_SIZE)
        self.is_map_loaded = True

    def has_map_loaded(self):
        return self.is_map_loaded
    def load_tileset(self, path_to_file_image):

        # Tile s image
        self.tileset_surface = pygame.image.load(path_to_file_image)

        self.check_loaded_tileset()

        self.tileset_surface.convert()
        self.path_to_tileset = path_to_file_image

    def is_rect_out_of_map_bounds(self, rect):
        return not self.rect_full_map.contains(rect)

    def clamp_rect(self, rect):
        return rect.clamp(self.rect_full_map)

    # Create a Surface that contains/draws all the visible tiles that are contained in rect_cut
    def create_image(self, rect_camera_map):
        # pre: rect_image must be created <TILE_SIZE*rows>X<TILE_SIZE*columns>
        assert self.is_map_loaded, "There's no map loaded yet!"

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

    def check_loaded_tileset(self):
        if normalize(self.tileset_surface.get_width(), TILE_SIZE) != self.tileset_surface.get_width() or \
                                self.tileset_surface.get_width() // TILE_SIZE < self.n_tiles or \
                        self.tileset_surface.get_height() != TILE_SIZE:
            raise AssertionError(
                'Wrong tileset, {0} must be width>={1} , height={2} and contain {3} different aligned tiles.'.
                format(self.path_to_tileset, self.n_tiles * TILE_SIZE, TILE_SIZE, self.n_tiles - 1))
