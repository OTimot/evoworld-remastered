import pygame
import sys

from engine.settings import FPS
from engine.window import Window
from engine.input import InputManager
from engine.assets import AssetManager
from engine.scene_manager import SceneManager

from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene

class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = Window()
        self.screen = self.window.screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.debug = False

        self.input = InputManager()
        self.assets = AssetManager()
        self.scenes = SceneManager()

        self.scenes.add_scene("menu", MenuScene(self))
        self.scenes.add_scene("game", GameScene(self))
        self.scenes.set_scene("menu")

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.window.toggle_fullscreen()
                        self.screen = self.window.screen

                    if event.key == pygame.K_F3:
                        self.debug = not self.debug

            self.input.update()
            self.scenes.handle_events(events)
            self.scenes.update(dt)
            self.scenes.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
