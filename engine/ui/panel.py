import pygame
from engine.ui.base import UIElement
from engine.ui.theme import DEFAULT_THEME

class UIPanel(UIElement):
    def __init__(self, rect, title="", font=None, theme=None):
        super().__init__(rect)
        self.title = title
        self.font = font
        self.theme = theme or DEFAULT_THEME
        self.children = []

    def add(self, element):
        self.children.append(element)
        return element

    def handle_event(self, event):
        if not self.visible or not self.enabled:
            return None
        for child in self.children:
            result = child.handle_event(event)
            if result is not None:
                return result
        return None

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, (0, 0, 0), self.rect.move(0, 8), border_radius=20)
        pygame.draw.rect(surface, self.theme.panel, self.rect, border_radius=20)
        pygame.draw.rect(surface, self.theme.border, self.rect, 2, border_radius=20)

        if self.title and self.font:
            title_img = self.font.render(self.title, True, self.theme.gold)
            surface.blit(title_img, (self.rect.x + 24, self.rect.y + 18))

        for child in self.children:
            child.draw(surface)
