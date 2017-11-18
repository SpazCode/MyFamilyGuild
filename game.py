#!/usr/bin/env python3

from components import util

from components.inputs import Inputs

from components.screen import Screen

import pygame

# Game Initialization
pygame.init()


class Game(object):

    # Constructor
    def __init__(self, settings_file):
        # Game loop flag.
        self.running = True
        # Load the game settings
        self.settings = util.load_json(settings_file)
        print(self.settings)

    # Flip the bit to colse the window.
    def close_window(self):
        print("Closing")
        self.running = False

    # The game loop.
    def run_game(self):
        # Load screen.
        screen = Screen(self.settings)
        # Set up controls.
        inputs = Inputs()
        inputs.set(pygame.QUIT, self.close_window)

        # Loop until we want to close the game.
        while self.running:
            # Check the inputs
            inputs.update(pygame.event.get())
            # Update the screen.
            screen.update()

if __name__ == "__main__":
    # Build the game.
    game = Game('settings.json')
    game.run_game()

# Deinitialze pygame when the game is over.
pygame.quit()
