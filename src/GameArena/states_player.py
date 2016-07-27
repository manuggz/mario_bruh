from src.GameEngine.animation import Animation
from pygame.locals import *


class State:
    def __init__(self, parent, x, y, frames, sprite_sheet):
        self.x, self.y = x, y
        self.parent = parent
        self.sprite_sheet = sprite_sheet
        self.animation = Animation(frames)

    def update(self, keys):
        self.animation.update()

    def get_frame(self):
        image = self.sprite_sheet.get(*self.animation.get_current_frame())
        rect = image.get_rect()
        rect.x = self.x - rect.w / 2
        rect.y = self.y - rect.h
        return image, rect


class WalkingRight(State):
    def __init__(self, parent, x, y, sprite_sheet):
        super().__init__(parent, x, y, [(1, 2), (1, 3), (1, 4), (1, 3)], sprite_sheet)

    def update(self, keys):
        super().update(keys)
        if keys[K_RIGHT]:
            self.x += 1
        else:
            self.parent.change_status(StandingRight(self.parent, self.x, self.y, self.sprite_sheet))


class WalkingLeft(State):
    def __init__(self, parent, x, y, sprite_sheet):
        super().__init__(parent, x, y, [(2, 13), (2, 12), (2, 11), (2, 12)], sprite_sheet)

    def update(self, keys):
        super().update(keys)
        if keys[K_LEFT]:
            self.x -= 1
        else:
            self.parent.change_status(StandingLeft(self.parent, self.x, self.y, self.sprite_sheet))


class StandingRight(State):
    def __init__(self, parent, x, y, sprite_sheet):
        super().__init__(parent, x, y, [(1, 1)], sprite_sheet)

    def update(self, keys):
        super().update(keys)
        if keys[K_RIGHT]:
            self.parent.change_status(WalkingRight(self.parent, self.x, self.y, self.sprite_sheet))
        elif keys[K_LEFT]:
            self.parent.change_status(WalkingLeft(self.parent, self.x, self.y, self.sprite_sheet))


class StandingLeft(State):
    def __init__(self, parent, x, y, sprite_sheet):
        super().__init__(parent, x, y, [(2, 14)], sprite_sheet)

    def update(self, keys):
        super().update(keys)
        if keys[K_RIGHT]:
            self.parent.change_status(WalkingRight(self.parent, self.x, self.y, self.sprite_sheet))
        elif keys[K_LEFT]:
            self.parent.change_status(WalkingLeft(self.parent, self.x, self.y, self.sprite_sheet))
