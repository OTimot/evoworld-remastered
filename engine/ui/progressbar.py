import pygame
from engine.ui.base import UIElement
from engine.ui.theme import DEFAULT_THEME

class UIProgressBar(UIElement):
    def __init__(self, rect, max_value=100, value=100, label="", theme=None):
        super().__init__(rect)
        self.max_value = max_value
        self.value = value
        self.label = label
        self.theme = theme or DEFAULT_THEME

    def set_value(self, value):
        self.value = max(0, min(self.max_value, value))

    def draw(self, surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, (5, 7, 12), self.rect, border_radius=10)
        ratio = 0 if self.max_value == 0 else self.value / self.max_value
        fill = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.w * ratio), self.rect.h)
        pygame.draw.rect(surface, self.theme.border, fill, border_radius=10)
        pygame.draw.rect(surface, self.theme.text, self.rect, 2, border_radius=10)
