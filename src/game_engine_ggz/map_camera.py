from pygame.locals import Rect

from src.game_engine_ggz.level_map_handler import MapHandler, create_camera_rect


# Controls  Camera(Rect that define what part of the map is showing on screen)
class MapCamera:
    def __init__(self, x_init_world, y_init_world, width_view_camera, height_view_camera):

        # rect that represents the surface visible of the camera
        self.rect_view_camera = Rect(x_init_world, y_init_world, width_view_camera, height_view_camera)

        self.pos_dest_screen = (0, 0)  # Position to draw the map captured by this Camera
        self.map_handler = None  # Controller of the map

        self.map_tile_surface = None  # Surface Buffer that contains the map drawn
        self.rect_hidden_camera = None  # Rect of the surface buffer with pos on map

        self.following = None
        self.can_follow = {"left": False, "top": False, "bottom": False, "right": True}

    # Start the camera setting buffers
    def init(self):
        assert self.map_handler is not None, "There's not a " + str(MapHandler.__class__) + " instance "
        assert self.map_handler.has_map_loaded(), "MapHandler has no map loaded yet!"
        self.__create_buffer()

    def __create_buffer(self):

        self.rect_hidden_camera = create_camera_rect(self.rect_view_camera, self.map_handler.get_tile_size())
        self.map_tile_surface = self.map_handler.create_image(self.rect_hidden_camera)

    def set_pos_screen(self, x_screen, y_screen):  # Set position to draw the map on screen
        self.pos_dest_screen = (x_screen, y_screen)

    def set_maphandler(self, map_handler):
        self.map_handler = map_handler

    # Move camera x y pixels
    def move(self, x_world, y_world):

        rect_moved = self.rect_view_camera.move(x_world, y_world)

        if self.map_handler.is_rect_out_of_map_bounds(rect_moved):
            return

        self.rect_view_camera.move_ip(x_world, y_world)

        if not self.rect_hidden_camera.contains(self.rect_view_camera):
            # If new pos is out of the buffer, we create a new one!
            self.__create_buffer()

    def draw(self, screen):

        rect_area_visible = Rect(self.rect_view_camera.x - self.rect_hidden_camera.x,
                                 self.rect_view_camera.y - self.rect_hidden_camera.y,
                                 self.rect_view_camera.width, self.rect_view_camera.height)
        screen.blit(self.map_tile_surface, self.pos_dest_screen, rect_area_visible)

    def get_x(self):
        return self.rect_view_camera.x

    def get_y(self):
        return self.rect_view_camera.y

    def follow(self, player):
        self.following = player

    def update(self):
        if self.following:
            x_p, y_p = self.following.x, \
                       self.following.y

            if self.can_follow['right']:
                if x_p > self.rect_view_camera.x + self.rect_view_camera.width / 4:
                    rect_moved = self.rect_view_camera.copy()
                    rect_moved.x = x_p - self.rect_view_camera.width / 4

                    if self.map_handler.is_rect_out_of_map_bounds(rect_moved):
                        return

                    self.rect_view_camera = rect_moved

                    if not self.rect_hidden_camera.contains(self.rect_view_camera):
                        # If new pos is out of the buffer, we create a new one!
                        self.__create_buffer()

    def is_rect_out_of_camera_bounds(self, rect):
        return not self.rect_view_camera.contains(rect)
