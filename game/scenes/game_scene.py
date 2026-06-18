import pygame
import math

from engine.scene import Scene
from engine.camera import Camera
from engine.settings import WHITE, GREEN, GOLD, RED, BLUE, PANEL

class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        w, h = app.window.get_size()
        self.camera = Camera(w, h)

        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 15)

        self.world_width = 3000
        self.world_height = 3000

        self.player = pygame.Rect(1500, 1500, 44, 44)
        self.player_speed = 280

        self.time = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.scenes.set_scene("menu")

    def update(self, dt):
        self.time += dt

        keys = self.app.input.keys

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        vec = pygame.Vector2(dx, dy)

        if vec.length_squared() > 0:
            vec = vec.normalize()
            self.player.x += int(vec.x * self.player_speed * dt)
            self.player.y += int(vec.y * self.player_speed * dt)

        self.player.x = max(0, min(self.world_width - self.player.width, self.player.x))
        self.player.y = max(0, min(self.world_height - self.player.height, self.player.y))

        sw, sh = self.app.window.get_size()
        self.camera.resize(sw, sh)
        self.camera.follow(self.player, dt)

    def draw_world_grid(self, screen):
        tile = 80
        start_x = int(self.camera.x // tile) * tile
        start_y = int(self.camera.y // tile) * tile

        sw, sh = screen.get_size()

        for y in range(start_y, start_y + sh + tile, tile):
            for x in range(start_x, start_x + sw + tile, tile):
                rect = pygame.Rect(x - self.camera.x, y - self.camera.y, tile, tile)

                biome_shift = int((math.sin((x + y) * 0.004) + 1) * 30)
                color = (35, 105 + biome_shift, 65)

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (25, 80, 50), rect, 1)

                if (x // tile + y // tile) % 7 == 0:
                    pygame.draw.circle(screen, (24, 120, 55), rect.center, 18)
                    pygame.draw.rect(screen, (95, 60, 35), (rect.centerx - 4, rect.centery + 10, 8, 22))

                if (x // tile - y // tile) % 11 == 0:
                    pygame.draw.circle(screen, (120, 120, 125), (rect.centerx + 18, rect.centery - 14), 10)

    def draw_player(self, screen):
        rect = self.camera.apply(self.player)

        pygame.draw.ellipse(screen, (0, 0, 0), (rect.x - 8, rect.y + 34, rect.width + 16, 14))
        pygame.draw.ellipse(screen, BLUE, rect)
        pygame.draw.ellipse(screen, (110, 210, 255), (rect.x + 8, rect.y + 6, rect.width - 16, rect.height - 12))

        pygame.draw.circle(screen, WHITE, (rect.centerx - 8, rect.centery - 5), 5)
        pygame.draw.circle(screen, WHITE, (rect.centerx + 8, rect.centery - 5), 5)
        pygame.draw.circle(screen, (0, 0, 0), (rect.centerx - 7, rect.centery - 5), 2)
        pygame.draw.circle(screen, (0, 0, 0), (rect.centerx + 9, rect.centery - 5), 2)

    def draw_hud(self, screen):
        sw, sh = screen.get_size()

        pygame.draw.rect(screen, PANEL, (0, 0, sw, 70))
        title = self.font.render("EvoWorld Remastered - Engine v0.0.1", True, GOLD)
        screen.blit(title, (20, 15))

        info = self.small_font.render("WASD mozgás | ESC menü | F11 fullscreen | F3 debug", True, WHITE)
        screen.blit(info, (20, 43))

        if self.app.debug:
            debug = f"DEBUG | FPS: {int(self.app.clock.get_fps())} | Player: {self.player.x}, {self.player.y} | Camera: {int(self.camera.x)}, {int(self.camera.y)}"
            txt = self.small_font.render(debug, True, GREEN)
            screen.blit(txt, (20, sh - 30))

    def draw(self, screen):
        screen.fill((5, 10, 15))
        self.draw_world_grid(screen)
        self.draw_player(screen)
        self.draw_hud(screen)
