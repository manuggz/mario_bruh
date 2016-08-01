class Animation:
    def __init__(self, frames, speed=5):
        self.set_frames(frames, speed)

    def update(self):
        self.count += 1

        if self.count >= self.speed:
            self.current_frame += 1
            if self.current_frame >= self.n_frames:
                self.current_frame = 0
            self.count = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def set_frames(self, frames, speed=5):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.count = 0
        self.n_frames = len(frames)
