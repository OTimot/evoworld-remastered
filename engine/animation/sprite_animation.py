class SpriteAnimation:
    def __init__(self, frames, fps=8, loop=True):
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.time = 0
        self.index = 0

    def reset(self):
        self.time = 0
        self.index = 0

    def update(self, dt):
        if not self.frames:
            return

        self.time += dt
        frame_time = 1 / self.fps

        while self.time >= frame_time:
            self.time -= frame_time
            self.index += 1

            if self.index >= len(self.frames):
                self.index = 0 if self.loop else len(self.frames) - 1

    def get_frame(self):
        if not self.frames:
            return None
        return self.frames[self.index]
