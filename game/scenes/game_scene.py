import pygame
import math
import random

from engine.scene import Scene
from engine.camera import Camera
from engine.settings import WHITE, GREEN, GOLD, BLUE, PANEL


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

        self.tile_size = 80
        self.vegetation = []
        self.vegetation_images = self.load_vegetation_images()
        self.generate_vegetation()

    def load_vegetation_images(self):
        images = []

        for key, image in self.app.assets.images.items():
            if key.startswith("sprites/vegetation/"):
                images.append(image)

        return images

    def generate_vegetation(self):
        random.seed(42)

        if not self.vegetation_images:
            return

        for _ in range(450):
            x = random.randint(80, self.world_width - 80)
            y = random.randint(80, self.world_height - 80)
            image = random.choice(self.vegetation_images)

            scale = random.choice([1.4, 1.7, 2.0, 2.3])
            w = int(image.get_width() * scale)
            h = int(image.get_height() * scale)
            scaled = pygame.transform.smoothscale(image, (w, h))

            self.vegetation.append({
                "x": x,
                "y": y,
                "image": scaled,
                "sort_y": y + h
            })

        self.vegetation.sort(key=lambda obj: obj["sort_y"])

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

    def draw_ground(self, screen):
        tile = self.tile_size
        start_x = int(self.camera.x // tile) * tile
        start_y = int(self.camera.y // tile) * tile
        sw, sh = screen.get_size()

        for y in range(start_y, start_y + sh + tile, tile):
            for x in range(start_x, start_x + sw + tile, tile):
                rect = pygame.Rect(x - self.camera.x, y - self.camera.y, tile, tile)
                biome_shift = int((math.sin((x + y) * 0.004) + 1) * 30)
                color = (35, 105 + biome_shift, 65)
                pygame.draw.rect(screen, color, rect)

    def draw_vegetation(self, screen):
        sw, sh = screen.get_size()

        for obj in self.vegetation:
            img = obj["image"]
            sx = obj["x"] - self.camera.x
            sy = obj["y"] - self.camera.y

            if sx < -160 or sy < -160 or sx > sw + 160 or sy > sh + 160:
                continue

            screen.blit(img, (sx - img.get_width() // 2, sy - img.get_height()))

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
        title = self.font.render("EvoWorld Remastered - Vegetation Test", True, GOLD)
        screen.blit(title, (20, 15))

        info = self.small_font.render(
            f"WASD mozgás | ESC menü | F11 fullscreen | F3 debug | Vegetation: {len(self.vegetation)}",
            True,
            WHITE
        )
        screen.blit(info, (20, 43))

        if self.app.debug:
            debug = (
                f"DEBUG | FPS: {int(self.app.clock.get_fps())} | "
                f"Player: {self.player.x}, {self.player.y} | "
                f"Camera: {int(self.camera.x)}, {int(self.camera.y)} | "
                f"Assets: {len(self.vegetation_images)}"
            )
            txt = self.small_font.render(debug, True, GREEN)
            screen.blit(txt, (20, sh - 30))

    def draw(self, screen):
        screen.fill((5, 10, 15))
        self.draw_ground(screen)
        self.draw_vegetation(screen)
        self.draw_player(screen)
        self.draw_hud(screen)