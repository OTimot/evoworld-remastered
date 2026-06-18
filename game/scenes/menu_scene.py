import pygame
import math

from engine.scene import Scene
from engine.settings import BG_COLOR, WHITE, GREEN, GOLD, PANEL, PANEL_LIGHT

class MenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.title_font = pygame.font.SysFont("arial", 76, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.time = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.app.scenes.set_scene("game")

                if event.key == pygame.K_ESCAPE:
                    self.app.running = False

    def update(self, dt):
        self.time += dt

    def draw_background(self, screen):
        w, h = screen.get_size()
        screen.fill(BG_COLOR)

        for i in range(12):
            x = int((i * 170 + self.time * 35) % (w + 200)) - 100
            y = int(h * 0.25 + math.sin(self.time + i) * 70 + i * 28)
            radius = 50 + (i % 4) * 18
            color = (18 + i * 3, 55 + i * 8, 65 + i * 5)
            pygame.draw.circle(screen, color, (x, y), radius)

        pygame.draw.circle(screen, (20, 100, 80), (w // 2, h // 2), 250, 3)
        pygame.draw.circle(screen, (40, 160, 110), (w // 2, h // 2), 160, 2)

    def draw(self, screen):
        self.draw_background(screen)

        w, h = screen.get_size()

        title = self.title_font.render("EVOWORLD", True, GREEN)
        subtitle = self.menu_font.render("Remastered", True, GOLD)
        version = self.small_font.render("v0.0.1 Engine alap", True, WHITE)

        screen.blit(title, (w // 2 - title.get_width() // 2, 135))
        screen.blit(subtitle, (w // 2 - subtitle.get_width() // 2, 220))
        screen.blit(version, (w // 2 - version.get_width() // 2, 265))

        button = pygame.Rect(w // 2 - 180, 350, 360, 62)
        pygame.draw.rect(screen, PANEL_LIGHT, button, border_radius=16)
        pygame.draw.rect(screen, GREEN, button, 3, border_radius=16)

        txt = self.menu_font.render("ENTER - Indítás", True, WHITE)
        screen.blit(txt, (button.centerx - txt.get_width() // 2, button.centery - txt.get_height() // 2))

        hint = self.small_font.render("F11 teljes képernyő | F3 debug | ESC kilépés", True, (180, 195, 205))
        screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 75))
