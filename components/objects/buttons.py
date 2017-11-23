#!/usr/bin/env python3
import pygame
from ..colors import Color
from display_object import DisplayObject
from ..text import Text


class Button(DisplayObject):
    # Constructor.
    def __init__(self, name, init_x=0, init_y=0, init_h=0, init_w=0,
                 callback=None, color=Color.GRAY, hover_color=Color.LIGHT_GRAY,
                 disabled_color=Color.DARK_GRAY, text_color=Color.BLACK,
                 text="", text_size=12, text_font="comicsanssms", enabled=True):
        super(Button, self).__init__(name, init_x, init_y, init_h, init_w)
        self.color = color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.text_color = text_color
        self.text_size = text_size
        self.callback = callback
        self.enabled = enabled
        self.text = Text(name + "_label", init_x, init_y, init_h, init_w,
                         font=text_font, size=text_size, text=text,
                         color=text_color)

    # Checks if the mouse is currently over the button on the screen.
    def on_hover(self):
        cur = pygame.mouse.get_pos()
        if self.x < cur[0] and + self.x + self.w > cur[0]:
            if self.y < cur[1] and self.y + self.h > cur[1]:
                return True
        return False

    # Check if the button has been clicked.
    def clicked(self):
        clicked = pygame.mouse.get_pressed()
        if self.on_hover() and clicked[0] == 1:
            return True
        else:
            return False

    # Draw the button to the screen
    def draw(self, display):
        if self.on_hover():
            pygame.draw.rect(display, self.hover_color,
                             (self.x, self.y, self.w, self.h))
        elif not self.enabled:
            pygame.draw.rect(display, self.disabled_color,
                             (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.color,
                             (self.x, self.y, self.w, self.h))
        self.text.draw(display)

    # Run the button callback if the button is clicked this frame.
    def update(self):
        if self.clicked() and self.enabled:
            self.callback()

    # Set the callback for the button.
    def set_callback(self, callback):
        self.callback = callback

    # Set the enabled state of the button.
    def set_enabled(self, enabled=True):
        self.enabled = enabled
