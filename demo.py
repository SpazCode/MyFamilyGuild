#!/usr/bin/env python3
import sys

import pygame

from engine.components.inputs import Inputs
from engine.components.objects.buttons import Button
from engine.components.objects.frames import Frame
from engine.components.objects.sprites import Sprite
from engine.components.objects.sprites import SpriteAnimationSet
from engine.components.scene import Scene
from engine.components.scene import SceneManager
from engine.game import Game

# Hack to load images early.
# It is ugly :S
pygame.display.set_mode((1, 1))


class TestScene(Scene):
    def __init__(self):
        # Scene variables.
        self.actor = None
        self.attacking = False
        # Build Scene components.
        super(TestScene, self).__init__()
        # Set Scene inputs.
        self.inputs.set(Inputs.CreateInputKey(
            "Pressed", pygame.K_LEFT), self.move_actor_left)
        self.inputs.set(Inputs.CreateInputKey(
            "Pressed", pygame.K_RIGHT), self.move_actor_right)
        self.inputs.set(Inputs.CreateInputKey(
            pygame.KEYDOWN, pygame.K_a), self.attack)

    def build(self):
        # Build the compoents in the scene.
        sprite = Sprite("test_background",
                        sprite_filepath="assets/sprites/background.png")
        sprite.scale(self.settings["screen"]["width"],
                     self.settings["screen"]["height"]).flip(x=True)
        self.add_component_background(sprite)
        # Loading skeleton framedata.
        animations = [("idle", "assets/data/skeleton/idle.json"),
                      ("attack", "assets/data/skeleton/attack.json")]
        self.actor = SpriteAnimationSet("skeleton", init_z=1,
                                        animations=animations)
        self.actor.scale(w_scale=4, h_scale=4).move_to(50, 300).set_on_finish("attack", self.return_to_idle)
        self.add_component_midground(self.actor)
        button = Button("btn_quit", init_z=0, init_x=25,
                        init_y=25, init_w=100, init_h=50, text="Quit")
        button.set_callback(self.quit_game)
        menu_frame = Frame("fme_menu", init_z=0, init_h=100, init_w=150,
                           init_x=((self.settings["screen"]["width"] / 2) - 75), init_y=400)\
            .add_components(button, 25, 25)
        self.add_component_foreground(menu_frame)

    def move_actor_right(self):
        if not self.attacking:
            self.actor.move_to(self.actor.x + 10, self.actor.y)

    def move_actor_left(self):
        if not self.attacking:
            self.actor.move_to(self.actor.x - 10, self.actor.y)

    def return_to_idle(self):
        self.attacking = False
        self.actor.set_animation("idle")

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.actor.set_animation("attack")

    def quit_game(self):
        sys.exit(1)


if __name__ == "__main__":
    manager = SceneManager()
    manager.add_scene("test", TestScene())
    manager.set_scene("test")
    game = Game("settings.json", scene_manager=manager)
    game.run_game()
