#!/usr/bin/env python3
import pygame
from colors import Color
from objects.display_object import DisplayObject


class Text(DisplayObject):

    def __init__(self, name, init_z=0, init_x=0, init_y=0, init_h=0, init_w=0,
                 font="comicsanssms", size=24, text="", color=Color.BLACK,
                 bold=False, underline=False):
        super(Text, self).__init__(
            name, init_z, init_x, init_y, init_h, init_w)
        if type(font).__name__ == "str":
            self.font = pygame.font.SysFont(font, size)
        else:
            self.font = font
        self.text = text
        self.color = color

    def draw(self, display):
        text = self.font.render(self.text, True, self.color)
        rect = text.get_rect()
        rect.center = self.get_center()
        display.blit(text, rect)

    def __copy__(self, text):
        return Text(self.name+"_copy", init_z=self.z, init_x=self.x,
                    init_y=self.y, init_h=self.h, init_w=self.w,
                    color=self.color, font=self.font)
