import pygame

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.smoothness = 8

    def resize(self, width, height):
        self.width = width
        self.height = height

    def follow(self, target_rect, dt):
        target_x = target_rect.centerx - self.width // 2
        target_y = target_rect.centery - self.height // 2

        self.x += (target_x - self.x) * min(1, self.smoothness * dt)
        self.y += (target_y - self.y) * min(1, self.smoothness * dt)

    def apply(self, rect):
        return pygame.Rect(
            rect.x - int(self.x),
            rect.y - int(self.y),
            rect.width,
            rect.height
        )
