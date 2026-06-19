import pygame
import random
import math

class Particle:
    def __init__(self, x, y, vx, vy, radius, color, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.life = life
        self.max_life = life

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.985
        self.vy *= 0.985

    def draw(self, screen):
        if self.life <= 0:
            return
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        size = max(1, int(self.radius * (self.life / self.max_life)))
        surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*self.color, alpha), (size * 2, size * 2), size)
        screen.blit(surface, (self.x - size * 2, self.y - size * 2))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_ambient(self, width, height, count=1):
        for _ in range(count):
            x = random.randint(0, width)
            y = random.randint(0, height)
            vx = random.uniform(-12, 12)
            vy = random.uniform(-32, -8)
            radius = random.uniform(2, 5)
            color = random.choice([(80, 230, 170), (80, 180, 255), (255, 220, 120)])
            life = random.uniform(2.5, 5.5)
            self.particles.append(Particle(x, y, vx, vy, radius, color, life))

    def burst(self, x, y, color, count=22):
        for _ in range(count):
            angle = random.random() * math.tau
            speed = random.uniform(50, 180)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            radius = random.uniform(3, 8)
            life = random.uniform(0.4, 1.1)
            self.particles.append(Particle(x, y, vx, vy, radius, color, life))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)