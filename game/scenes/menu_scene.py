import pygame
import math
import random

from engine.scene import Scene
from engine.settings import *
from engine.ui import UIManager, UIButton, UIPanel
from engine.fx.particles import ParticleSystem

class MenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)

        self.title_font = pygame.font.SysFont("arial", 84, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 30, bold=True)
        self.button_font = pygame.font.SysFont("arial", 26, bold=True)
        self.small_font = pygame.font.SysFont("arial", 17)

        self.time = 0
        self.particles = ParticleSystem()
        self.ui = UIManager()
        self.rebuild_ui()

    def rebuild_ui(self):
        self.ui.clear()
        w, h = self.app.window.get_size()

        panel_w = 430
        panel_h = 275
        panel = UIPanel(
            (w // 2 - panel_w // 2, int(h * 0.43), panel_w, panel_h),
            title="Főmenü",
            font=self.subtitle_font
        )

        bx = panel.rect.x + 35
        by = panel.rect.y + 74
        bw = panel.rect.w - 70
        bh = 56

        panel.add(UIButton("ÚJ JÁTÉK", (bx, by, bw, bh), self.button_font, "play"))
        panel.add(UIButton("BEÁLLÍTÁSOK", (bx, by + 70, bw, bh), self.button_font, "settings"))
        panel.add(UIButton("KILÉPÉS", (bx, by + 140, bw, bh), self.button_font, "quit"))
        self.ui.add(panel)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.rebuild_ui()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.app.scenes.set_scene("game")
                if event.key == pygame.K_ESCAPE:
                    self.app.running = False

        action = self.ui.handle_events(events)
        if action == "play":
            w, h = self.app.window.get_size()
            self.particles.burst(w // 2, h // 2, GREEN, 60)
            self.app.scenes.set_scene("game")
        elif action == "settings":
            w, h = self.app.window.get_size()
            self.particles.burst(w // 2, h // 2, GOLD, 38)
        elif action == "quit":
            self.app.running = False

    def update(self, dt):
        self.time += dt
        w, h = self.app.window.get_size()
        if random.random() < 0.45:
            self.particles.spawn_ambient(w, h, 1)
        self.particles.update(dt)
        self.ui.update(dt)

    def draw_background(self, screen):
        w, h = screen.get_size()
        screen.fill((6, 10, 18))

        bg = self.app.assets.get_image("backgrounds/menu")
        if bg:
            bg = pygame.transform.smoothscale(bg, (w, h))
            screen.blit(bg, (0, 0))
            return

        for y in range(0, h, 4):
            t = y / max(1, h)
            color = (int(6 + 12 * t), int(10 + 28 * t), int(18 + 36 * t))
            pygame.draw.rect(screen, color, (0, y, w, 4))

        for i in range(13):
            x = int((i * 175 + self.time * 32) % (w + 240)) - 120
            y = int(h * 0.19 + math.sin(self.time * 0.9 + i) * 60 + i * 22)
            radius = 60 + (i % 4) * 22
            color = (8 + i * 3, 48 + i * 8, 58 + i * 7)
            pygame.draw.circle(screen, color, (x, y), radius)

        pulse = int(math.sin(self.time * 2) * 20)
        pygame.draw.circle(screen, (40, 190, 130), (w // 2, h // 2), 285 + pulse, 2)
        pygame.draw.circle(screen, (80, 230, 170), (w // 2, h // 2), 190 - pulse, 2)

    def draw_title(self, screen):
        w, h = screen.get_size()
        title = self.title_font.render("EVOWORLD", True, GREEN)
        shadow = self.title_font.render("EVOWORLD", True, (0, 0, 0))
        subtitle = self.subtitle_font.render("Remastered", True, GOLD)
        float_y = int(math.sin(self.time * 2.2) * 8)

        screen.blit(shadow, (w // 2 - title.get_width() // 2 + 5, 80 + float_y + 5))
        screen.blit(title, (w // 2 - title.get_width() // 2, 80 + float_y))
        screen.blit(subtitle, (w // 2 - subtitle.get_width() // 2, 172 + float_y))
        version = self.small_font.render(f"{VERSION}  |  F11 fullscreen  |  F3 debug", True, TEXT_MUTED)
        screen.blit(version, (w // 2 - version.get_width() // 2, 213 + float_y))

    def draw_footer(self, screen):
        w, h = screen.get_size()
        summary = self.app.assets.debug_summary()
        text = f"EvoEngine v0.1.3 - Asset Manager | IMG {summary['images']} | SND {summary['sounds']} | FONT {summary['fonts']}"
        img = self.small_font.render(text, True, TEXT_MUTED)
        screen.blit(img, (w // 2 - img.get_width() // 2, h - 52))

        if self.app.debug:
            debug = f"FPS: {int(self.app.clock.get_fps())} | Particles: {len(self.particles.particles)} | UI: {len(self.ui.elements)}"
            dbg = self.small_font.render(debug, True, CYAN)
            screen.blit(dbg, (18, h - 32))

    def draw(self, screen):
        self.draw_background(screen)
        self.particles.draw(screen)
        self.draw_title(screen)
        self.ui.draw(screen)
        self.draw_footer(screen)
