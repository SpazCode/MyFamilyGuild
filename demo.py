#!/usr/bin/env python3
import pygame
from engine.game import Game
from engine.components import util
from engine.components.inputs import Inputs
from engine.components.scene import Scene
from engine.components.scene import SceneManager
from engine.components.objects.buttons import Button
from engine.components.objects.sprites import FrameData
from engine.components.objects.sprites import Sprite
from engine.components.objects.sprites import SpriteAnimation
from engine.components.objects.sprites import SpriteSheetManager

# Hack to load images early.
# It is ugly :S
pygame.display.set_mode((1, 1))


class TestScene(Scene):

    def __init__(self):
        # Scene variables.
        self.actor = None
        # Build Scene components.
        super(TestScene, self).__init__()
        # Set Scene inputs.
        self.inputs.set(Inputs.CreateInputKey(
            pygame.KEYDOWN, pygame.K_LEFT), self.move_actor_left)
        self.inputs.set(Inputs.CreateInputKey(
            pygame.KEYDOWN, pygame.K_RIGHT), self.move_actor_right)

    def build(self):
        # Loading skeleton framedata.
        frame_data = FrameData(util.load_json(
            "assets/data/skeleton/idle.json"))
        # Load demo sprite sheet.
        manager = SpriteSheetManager(
            "assets/sprites/skeleton/Skeleton Idle.png", transparent=True)
        # Build the compoents in the scene.
        button = Button("test_button", init_z=0, init_x=50,
                        init_y=50, init_w=100, init_h=50, text="Testing")
        self.add_component_midground(button)
        sprite = Sprite("test_background",
                        sprite_filepath="assets/sprites/background.png")
        sprite.scale(self.settings["screen"]["width"],
                     self.settings["screen"]["height"]).flip(x=True)
        self.add_component_background(sprite)
        anim = SpriteAnimation("skeleton_idle", init_z=1, init_x=0,
                               init_y=0, frame_data=frame_data,
                               sprite_sheet=manager)
        anim.scale(w_multi=4, h_multi=4)
        anim.move_to(0, 32*4)
        self.add_component_midground(anim)
        self.actor = anim

    def move_actor_right(self):
        self.actor.x += 10

    def move_actor_left(self):
        self.actor.x -= 10


if __name__ == "__main__":
    manager = SceneManager()
    manager.add_scene("test", TestScene())
    manager.set_scene("test")
    game = Game("settings.json", scene_manager=manager)
    game.run_game()
