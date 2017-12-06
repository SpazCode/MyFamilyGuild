#!/usr/bin/env python3
import pygame
from engine.game import Game
from engine.components.scene import Scene
from engine.components.scene import SceneManager
from engine.components.objects.buttons import Button
from engine.components.objects.sprites import Sprite

# Hack to load images early.
# It is ugly :S
pygame.display.set_mode((1, 1))


class TestScene(Scene):

    def __init__(self):
        super(TestScene, self).__init__()

    def build(self):
        button = Button("test_button", init_z=0, init_x=50,
                        init_y=50, init_w=100, init_h=50, text="Testing")
        self.add_component_midground(button)
        sprite = Sprite("test_background",
                        sprite_filepath="assets/sprites/background.png")
        sprite = sprite.scale(self.settings["screen"]["width"],
                              self.settings["screen"]["height"]).flip(x=True)
        self.add_component_background(sprite)

if __name__ == "__main__":
    manager = SceneManager()
    manager.add_scene("test", TestScene())
    manager.set_scene("test")
    game = Game("settings.json", scene_manager=manager)
    game.run_game()
