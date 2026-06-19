import os
import pygame

class AssetManager:
    IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
    SOUND_EXTENSIONS = (".wav", ".ogg", ".mp3")
    FONT_EXTENSIONS = (".ttf", ".otf")

    def __init__(self, root_path="assets"):
        self.root_path = root_path
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.missing_image = None

    def initialize(self):
        self._create_missing_image()
        self.scan_assets()

    def _create_missing_image(self):
        surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        surface.fill((180, 40, 180))
        pygame.draw.line(surface, (20, 20, 20), (0, 0), (64, 64), 5)
        pygame.draw.line(surface, (20, 20, 20), (64, 0), (0, 64), 5)
        self.missing_image = surface

    def normalize_key(self, path):
        path = path.replace("\\", "/")
        if path.startswith(self.root_path + "/"):
            path = path[len(self.root_path) + 1:]
        return os.path.splitext(path)[0].lower()

    def scan_assets(self):
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path, exist_ok=True)
            return

        for root, _, files in os.walk(self.root_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                ext = os.path.splitext(filename)[1].lower()

                if ext in self.IMAGE_EXTENSIONS:
                    self.load_image(full_path)
                elif ext in self.SOUND_EXTENSIONS:
                    self.load_sound(full_path)
                elif ext in self.FONT_EXTENSIONS:
                    self.register_font(full_path)

    def load_image(self, path, key=None, scale=None):
        if not os.path.exists(path):
            return self.missing_image

        key = key or self.normalize_key(path)

        if key in self.images and scale is None:
            return self.images[key]

        try:
            image = pygame.image.load(path).convert_alpha()
            if scale:
                image = pygame.transform.smoothscale(image, scale)
            self.images[key] = image
            return image
        except pygame.error:
            self.images[key] = self.missing_image
            return self.missing_image

    def get_image(self, key, scale=None):
        image = self.images.get(key.lower())
        if image is None:
            return self.missing_image
        if scale:
            return pygame.transform.smoothscale(image, scale)
        return image

    def load_sound(self, path, key=None):
        if not os.path.exists(path):
            return None

        key = key or self.normalize_key(path)

        if key in self.sounds:
            return self.sounds[key]

        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[key] = sound
            return sound
        except pygame.error:
            return None

    def get_sound(self, key):
        return self.sounds.get(key.lower())

    def register_font(self, path, key=None):
        if not os.path.exists(path):
            return None
        key = key or self.normalize_key(path)
        self.fonts[key] = path
        return path

    def get_font(self, key, size=24):
        path = self.fonts.get(key.lower())
        if path:
            return pygame.font.Font(path, size)
        return pygame.font.SysFont("arial", size)

    def debug_summary(self):
        return {
            "images": len(self.images),
            "sounds": len(self.sounds),
            "fonts": len(self.fonts)
        }
