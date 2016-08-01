import pygame
from pygame.locals import SRCALPHA, Rect


def normalize(n, unit):
    return (n // unit) * unit


def create_camera_rect(rect_camera_visible, tile_size):
    rect_camera_map = rect_camera_visible.copy()
    rect_camera_map.x = normalize(rect_camera_visible.x, tile_size)
    rect_camera_map.y = normalize(rect_camera_visible.y, tile_size)

    rect_camera_map.width = normalize(rect_camera_visible.right, tile_size) - rect_camera_map.x
    if rect_camera_visible.right > rect_camera_map.right:
        rect_camera_map.width += tile_size

    rect_camera_map.height = normalize(rect_camera_visible.bottom, tile_size) - rect_camera_map.y
    if rect_camera_visible.bottom > rect_camera_map.bottom:
        rect_camera_map.height += tile_size

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
    def __init__(self, tile_size):

        self.matrix_tiles = None
        self.rect_full_map = None
        self.tileset_surface = None
        self.is_map_loaded = False
        self.n_rows = 0
        self.n_cols = 0
        self.n_tiles = 0
        self.path_to_tileset = None
        self.tile_size = tile_size

    # Load a file containing tile positioning
    def load_map(self, path_to_file_level):

        # Tile s positioning data
        file_level = open(path_to_file_level)

        self.matrix_tiles = []
        # lines = file_level.readlines()
        # n_lines = len(lines)
        self.n_rows, self.n_cols, self.n_tiles = read_n_rows_columns_num_tiles(file_level)

        if self.is_map_loaded:
            self.check_loaded_tileset()  # We check that we can cover the tiles with our current
        # tile set

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
        self.rect_full_map = Rect(0, 0, self.n_cols * self.tile_size, self.n_rows * self.tile_size)
        self.is_map_loaded = True

    def clamp_rect(self, rect):
        return rect.clamp(self.rect_full_map)

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

    # Create a Surface that contains/draws all the visible tiles that are contained in rect_cut
    def create_image(self, rect_camera_map):
        # pre: rect_image must be created <TILE_SIZE*rows>X<TILE_SIZE*columns>
        assert self.is_map_loaded, "There's no map loaded yet!"

        image_map_tile = pygame.Surface(rect_camera_map.size, SRCALPHA)

        n_rows = rect_camera_map.height // self.tile_size
        n_columns = rect_camera_map.width // self.tile_size

        i_init_matriz = rect_camera_map.y // self.tile_size
        j_init_matriz = rect_camera_map.x // self.tile_size

        src_srfc_tile_rect = Rect(0, 0, self.tile_size, self.tile_size)

        for i in range(n_rows):

            i_matrix = i_init_matriz + i
            if i_matrix >= self.n_rows:
                continue

            for j in range(n_columns):

                j_matrix = j_init_matriz + j

                if j_matrix >= self.n_cols:
                    continue

                tile_index = self.matrix_tiles[i_matrix][j_matrix]

                if tile_index != 0:
                    src_srfc_tile_rect.x = self.tile_size * (tile_index - 1)
                    image_map_tile.blit(self.tileset_surface, (
                        (j_matrix - j_init_matriz) * self.tile_size, (i_matrix - i_init_matriz) * self.tile_size),
                                        src_srfc_tile_rect)

        return image_map_tile

    def check_loaded_tileset(self):
        if normalize(self.tileset_surface.get_width(), self.tile_size) != self.tileset_surface.get_width() or \
                                self.tileset_surface.get_width() // self.tile_size < (
                            self.n_tiles - 1) or self.tileset_surface.get_height() != self.tile_size:
            raise AssertionError(
                'Wrong tileset, {0} must be width>={1} , height={2} and contain {3} different aligned tiles.'.format(
                    self.path_to_tileset, self.n_tiles * self.tile_size, self.tile_size, self.n_tiles - 1))

    def collide_map(self, rect):
        assert self.is_map_loaded, "There's no map loaded yet!"

        rect_collide = create_camera_rect(rect, self.tile_size)

        n_rows = rect_collide.height // self.tile_size
        n_columns = rect_collide.width // self.tile_size

        i_init_matriz = rect_collide.y // self.tile_size
        j_init_matriz = rect_collide.x // self.tile_size

        collide_list = []
        for i in range(n_rows):

            i_matrix = i_init_matriz + i
            if i_matrix >= self.n_rows:
                continue

            for j in range(n_columns):

                j_matrix = j_init_matriz + j

                if j_matrix >= self.n_cols:
                    continue

                tile_index = self.matrix_tiles[i_matrix][j_matrix]

                if tile_index != 0:
                    collide_list.append((tile_index, (i, j)))

        return collide_list

    def get_tile_size(self):
        return self.tile_size

    def get_floor_dist(self, x, y, max_dist):
        """Obtiene la distancia entre el punto (x, y) y el proximo bloque solido hacia abajo"""

        for dy in range(max_dist):
            if (y + dy) % self.tile_size == 0 and self.matrix_tiles[int((y + dy) // self.tile_size)][
                        x // self.tile_size] != 0:
                return dy

        return max_dist

    def get_nearest_bottom_tile(self, rect, max_deep):
        """"Regresa el primer tile que se encuentre hacia abajo"""

        rect_collide = create_camera_rect(rect, self.tile_size)

        n_columns = rect_collide.width // self.tile_size

        i_init_matriz = rect_collide.bottom // self.tile_size
        j_init_matriz = rect_collide.x // self.tile_size

        for i in range(max_deep):

            i_matrix = i_init_matriz + i
            if i_matrix >= self.n_rows:
                return None

            for j in range(n_columns):

                j_matrix = j_init_matriz + j

                if j_matrix >= self.n_cols:
                    break

                tile_index = self.matrix_tiles[i_matrix][j_matrix]

                if tile_index != 0:
                    return tile_index, (i_matrix, j_matrix), rect_collide.bottom - rect.bottom + i * self.tile_size

        return None
