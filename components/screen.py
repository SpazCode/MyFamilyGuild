#!/usr/bin/env python3
import pygame
from objects.buttons import Button


class Screen(object):
    """ Constructor

        Description: Wrapper around the Pygame display objects.
                     Creates screen object to manage creating screens
                     and updating them.

        Parameters: pygmae - the current pygame object from the game.py
                    title - the title of the game to put on the window
                    screen_size - the width, height tuple for the screen
                                  dimentions
    """

    def __init__(self, settings):
        self.__fps = settings['fps']
        self.__clock = pygame.time.Clock()
        self.__last_wait = 0
        self.__display = pygame.display.set_mode(
            (settings['screen']['width'], settings['screen']['height']))
        pygame.display.set_caption(settings['title'])
        pygame.display.set_icon(
            pygame.image.load(settings['icon']))

    """ Return the games current display. """
    def get_display(self):
        return self.__display

    """ Update the screen. """
    def update(self):
        pygame.display.update()
        self.__last_wait = self.__clock.tick(self.__fps)
