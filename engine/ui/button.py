import pygame
from engine.ui.base import UIElement
from engine.ui.theme import DEFAULT_THEME

class UIButton(UIElement):
    def __init__(self, text, rect, font, action=None, theme=None):
        super().__init__(rect)
        self.text = text
        self.font = font
        self.action = action
        self.theme = theme or DEFAULT_THEME
        self.anim = 0.0
        self.pressed = False

    def handle_event(self, event):
        if not self.visible or not self.enabled:
            return None

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.pressed
            self.pressed = False
            if was_pressed and self.rect.collidepoint(event.pos):
                return self.action

        return None

    def update(self, dt):
        target = 1.0 if self.hovered else 0.0
        self.anim += (target - self.anim) * min(1, dt * 14)

    def draw(self, surface):
        if not self.visible:
            return

        grow = int(self.anim * 8)
        rect = self.rect.inflate(grow, grow)
        if self.pressed:
            rect = rect.move(0, 3)

        color = (
            int(self.theme.panel_light[0] + (self.theme.border[0] - self.theme.panel_light[0]) * self.anim),
            int(self.theme.panel_light[1] + (self.theme.border[1] - self.theme.panel_light[1]) * self.anim),
            int(self.theme.panel_light[2] + (self.theme.border[2] - self.theme.panel_light[2]) * self.anim),
        )

        pygame.draw.rect(surface, (0, 0, 0), rect.move(0, 7), border_radius=18)
        pygame.draw.rect(surface, color, rect, border_radius=18)
        pygame.draw.rect(surface, self.theme.border, rect, 2, border_radius=18)

        text_color = self.theme.text if self.hovered else self.theme.muted
        img = self.font.render(self.text, True, text_color)
        surface.blit(img, (rect.centerx - img.get_width() // 2, rect.centery - img.get_height() // 2))
