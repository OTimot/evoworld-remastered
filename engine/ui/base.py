import pygame

class UIElement:
    def __init__(self, rect, visible=True, enabled=True):
        self.rect = pygame.Rect(rect)
        self.visible = visible
        self.enabled = enabled
        self.hovered = False
        self.focused = False

    def handle_event(self, event):
        return None

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def center_on(self, x, y):
        self.rect.center = (x, y)
