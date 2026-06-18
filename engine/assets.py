import pygame
import os

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, name, path, scale=None):
        if not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()

        if scale:
            image = pygame.transform.smoothscale(image, scale)

        self.images[name] = image
        return image

    def get_image(self, name):
        return self.images.get(name)

    def load_sound(self, name, path):
        if not os.path.exists(path):
            return None

        sound = pygame.mixer.Sound(path)
        self.sounds[name] = sound
        return sound

    def get_sound(self, name):
        return self.sounds.get(name)
