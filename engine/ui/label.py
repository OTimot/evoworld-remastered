import pygame
from engine.ui.base import UIElement
from engine.ui.theme import DEFAULT_THEME

class UILabel(UIElement):
    def __init__(self, text, x, y, font, color=None, center=False):
        self.text = text
        self.font = font
        self.color = color or DEFAULT_THEME.text
        self.center = center
        image = self.font.render(self.text, True, self.color)
        rect = image.get_rect()
        rect.topleft = (x, y)
        super().__init__(rect)

    def set_text(self, text):
        self.text = text

    def draw(self, surface):
        if not self.visible:
            return
        image = self.font.render(self.text, True, self.color)
        rect = image.get_rect()
        if self.center:
            rect.center = self.rect.center
        else:
            rect.topleft = self.rect.topleft
        surface.blit(image, rect)
