#!/usr/bin/env python3
import sys
sys.path.insert(
    0, '/mnt/Data/Stuart/Projects/Python/pygame/rpg/engine/components')

import pygame
from colors import Color
from display_object import DisplayObject
from text import Text


class Button(DisplayObject):

    # Constructor.
    def __init__(self, name, init_z=0, init_x=0, init_y=0, init_h=50, init_w=100,
                 callback=None, color=Color.GRAY, hover_color=Color.LIGHT_GRAY,
                 disabled_color=Color.DARK_GRAY, text_color=Color.BLACK,
                 text="", text_size=32, text_font="comicsanssms",
                 enabled=True):
        super(Button, self).__init__(name=name, init_z=init_z,
                                     init_x=init_x, init_y=init_y,
                                     init_h=init_h, init_w=init_w,
                                     origin_x=0, origin_y=0,)
        self._background_color = color
        self.color = color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.text_color = text_color
        self.text_size = text_size
        self.callback = callback
        self.enabled = enabled
        self.text = Text(name + "_label", init_z=init_z, init_x=init_x, init_y=init_y, init_h=init_h,
                         init_w=init_w, font=text_font, size=text_size, text=text, color=text_color)

    # Checks if the mouse is currently over the button on the screen.
    def on_hover(self):
        cur = pygame.mouse.get_pos()
        if self.x < cur[0] and + self.x + self.w > cur[0]:
            if self.y < cur[1] and self.y + self.h > cur[1]:
                return True
        return False

    # Check if the button has been clicked.
    def clicked(self):
        # Set background color.
        if self.on_hover():
            self._background_color = self.hover_color
        elif not self.enabled:
            self._background_color = self.disabled_color
        else:
            self._background_color = self.color
        # Get User interaction.
        clicked = pygame.mouse.get_pressed()
        if self.on_hover() and clicked[0] == 1:
            return True
        else:
            return False

    # Draw the button to the screen
    def draw(self, display):
        pygame.draw.rect(display, self._background_color,
                         (self.x, self.y, self.w, self.h))
        self.text.draw(display)

    # Run the button callback if the button is clicked this frame.
    def update(self):
        if self.clicked() and self.enabled and self.callback is not None:
            self.callback()

    # Set the callback for the button.
    def set_callback(self, callback):
        self.callback = callback

    # Set the enabled state of the button.
    def set_enabled(self, enabled=True):
        self.enabled = enabled
