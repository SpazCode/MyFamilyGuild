#!/usr/bin/env python3
from components import util
from components.screen import Screen
import pygame

# Game Initialization
pygame.init()


class Game(object):

    # Constructor
    def __init__(self, settings_file, scene_manager=None):
        # Game loop flag.
        self.running = True
        # Load the game settings
        self.settings = util.load_json(settings_file)
        print(self.settings)
        self.scene_manager = scene_manager
        # Load screen.
        self.screen = Screen(self.settings)
        # Inform the scenes of the screen and settings.
        if self.scene_manager is not None:
            self.scene_manager.set_screen(self.screen)
            self.scene_manager.set_settings(self.settings)
            self.scene_manager.build_scenes()

    # Flip the bit to colse the window.
    def close_window(self):
        print("Closing")
        self.running = False

    # The game loop.
    def run_game(self):
        # Loop until we want to close the game.
        while self.running:
            # Clear the screen.
            self.screen.clear()
            # Update the Scene then draw it.
            if self.scene_manager is not None:
                self.scene_manager.update()
            # Update the Screen.
            self.screen.update()
            # Check if someone wants to close the window.
            for event in pygame.event.get(pygame.QUIT):
                if event.type == pygame.QUIT:
                    self.close_window()

        # Deinitialze pygame when the game is over.
        pygame.quit()
