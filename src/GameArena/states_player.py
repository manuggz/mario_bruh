from pygame.locals import *

from src.game_engine_ggz.animation import Animation


class State:
    def __init__(self, player, frames):
        self.player = player
        self.animation = Animation(frames)

    def update(self, keys):
        self.animation.update()


class WalkingRight(State):
    def __init__(self, player):
        super().__init__(player, [(1, 2), (1, 3), (1, 4), (1, 3)])

    def update(self, keys):
        super().update(keys)
        if keys[K_RIGHT]:
            self.player.move(self.player.move_speed, 0)
            if self.player.is_out_of_screen_bounds() or self.player.collide_map():
                self.player.move(-self.player.move_speed, 0)

            if not self.player.has_solid_bottom():
                self.player.change_state(Falling(self.player, [(1, 3)]))
        else:
            self.player.change_state(StandingRight(self.player))

        if (keys[K_SPACE] or keys[K_UP]) and not self.player.jump_pressed:
            self.player.change_state(Jumping(self.player, self.player.jump_power, [(1, 6)]))
        elif not (keys[K_SPACE] or keys[K_UP]):
            self.player.jump_pressed = False


class WalkingLeft(State):
    def __init__(self, player):
        super().__init__(player, [(2, 13), (2, 12), (2, 11), (2, 12)])

    def update(self, keys):
        super().update(keys)
        if keys[K_LEFT]:
            self.player.move(-self.player.move_speed, 0)
            if self.player.is_out_of_screen_bounds() or self.player.collide_map():
                self.player.move(self.player.move_speed, 0)

            if not self.player.has_solid_bottom():
                self.player.change_state(Falling(self.player, [(2, 12)]))

        else:
            self.player.change_state(StandingLeft(self.player))

        if (keys[K_SPACE] or keys[K_UP]) and not self.player.jump_pressed:
            self.player.change_state(Jumping(self.player, self.player.jump_power, [(2, 9)]))
        elif not (keys[K_SPACE] or keys[K_UP]):
            self.player.jump_pressed = False


class Falling(State):
    def __init__(self, player, frames):
        super().__init__(player, frames)
        self.acceleration = 0.3
        self.max_speed = 5
        self.speed = self.player.move_speed

    def update(self, keys):
        super().update(keys)

        try:
            dy = self.player.get_floor_dist(self.max_speed)
        except IndexError:
            self.player.change_state(StandingRight(self.player))
            return

        if dy == 0:
            if self.animation.get_current_frame()[0] == 1:
                self.player.change_state(StandingRight(self.player))
            else:
                self.player.change_state(StandingLeft(self.player))
            return

        if dy > int(self.speed):
            self.player.move(0, int(self.speed))
            self.speed += self.acceleration
            if self.speed >= self.max_speed:
                self.acceleration = 0
                self.speed = self.max_speed
        else:
            self.player.move(0, dy)


class StandingRight(State):
    def __init__(self, player):
        super().__init__(player, [(1, 1)])

    def update(self, keys):
        super().update(keys)

        if keys[K_RIGHT]:
            self.player.change_state(WalkingRight(self.player))
        elif keys[K_LEFT]:
            self.player.change_state(WalkingLeft(self.player))

        if (keys[K_SPACE] or keys[K_UP]) and not self.player.jump_pressed:
            self.player.change_state(Jumping(self.player, self.player.jump_power + 0.2, [(1, 6)]))
        elif not (keys[K_SPACE] or keys[K_UP]):
            self.player.jump_pressed = False


class StandingLeft(State):
    def __init__(self, player):
        super().__init__(player, [(2, 14)])

    def update(self, keys):
        super().update(keys)
        if keys[K_RIGHT]:
            self.player.change_state(WalkingRight(self.player))
        elif keys[K_LEFT]:
            self.player.change_state(WalkingLeft(self.player))

        if (keys[K_SPACE] or keys[K_UP]) and not self.player.jump_pressed:
            self.player.change_state(Jumping(self.player, self.player.jump_power + 0.2, [(2, 9)]))
        elif not (keys[K_SPACE] or keys[K_UP]):
            self.player.jump_pressed = False


class Jumping(State):
    """Representa el estado 'saltando'"""

    def __init__(self, player, vy, frames):
        """Inicia un salto con velocidad inicial indicada por el parametro vy"""

        super().__init__(player, frames)
        self.vy = vy
        self.player.jump_pressed = True

    def update(self, keys):
        super().update(keys)
        self.vy += 0.2
        dy = int(self.vy)

        if dy > 0:
            dy = self.player.get_floor_dist(int(self.vy))

            if self.player.has_solid_bottom():

                if self.animation.get_current_frame()[0] == 1:
                    self.player.change_state(StandingRight(self.player))
                else:
                    self.player.change_state(StandingLeft(self.player))

        if keys[K_LEFT]:
            self.player.move(-self.player.move_speed, 0)
            if self.player.is_out_of_screen_bounds() or self.player.collide_map():
                self.player.move(+self.player.move_speed, 0)

        elif keys[K_RIGHT]:
            self.player.move(self.player.move_speed, 0)
            if self.player.is_out_of_screen_bounds() or self.player.collide_map():
                self.player.move(-self.player.move_speed, 0)

        self.player.move(0, dy)

        collide_tiles = self.player.collide_map()
        if collide_tiles:
            self.player.move(0, -dy)
            self.vy = 0
