class Interface:
    def __init__(self, parent):
        self.parent = parent

    def draw(self, screen):
        pass

    def update(self, keys):
        pass

    def update_draw(self, screen):
        pass
