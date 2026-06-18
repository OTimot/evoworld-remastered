import pygame

class InputManager:
    def __init__(self):
        self.keys = None
        self.mouse_pos = (0, 0)
        self.mouse_buttons = None

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()

    def pressed(self, key):
        return self.keys[key] if self.keys else False
