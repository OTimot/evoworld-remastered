import pygame

from engine.animation import SpriteAnimation

class Player:
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.width = 52
        self.height = 52
        self.speed = 280
        self.facing_right = True
        self.moving = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.idle_animation = SpriteAnimation(
            self.load_frames("sprites/player/evo_cell/idle", "idle", 4, (96, 96)),
            fps=5
        )

        self.walk_animation = SpriteAnimation(
            self.load_frames("sprites/player/evo_cell/walk", "walk", 6, (96, 96)),
            fps=10
        )

        self.current_animation = self.idle_animation

    def load_frames(self, folder_key, prefix, count, scale):
        frames = []
        for i in range(count):
            key = f"{folder_key}/{prefix}_{i}"
            image = self.app.assets.get_image(key, scale=scale)
            frames.append(image)
        return frames

    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self, dt):
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
        self.moving = vec.length_squared() > 0

        if self.moving:
            vec = vec.normalize()
            self.x += vec.x * self.speed * dt
            self.y += vec.y * self.speed * dt

            if vec.x > 0:
                self.facing_right = True
            elif vec.x < 0:
                self.facing_right = False

        self.current_animation = self.walk_animation if self.moving else self.idle_animation
        self.current_animation.update(dt)
        self.update_rect()

    def draw(self, screen, camera):
        image = self.current_animation.get_frame()
        if image is None:
            return

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        screen_x = self.x - camera.x + self.width // 2 - image.get_width() // 2
        screen_y = self.y - camera.y + self.height - image.get_height() + 8

        screen.blit(image, (screen_x, screen_y))
