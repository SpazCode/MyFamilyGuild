#!/usr/bin/env python3
import os
import pygame
from display_object import DisplayObject


class Sprite(DisplayObject):

    def __init__(self, name, init_z=0, init_x=0, init_y=0,
                 init_cx=0, init_cy=0, sprite_surface=None,
                 sprite_filepath=None):
        super(Sprite, self).__init__(
            name, init_z, init_x, init_y, 0, 0)
        self.image = None
        self.sprite_filepath = None
        self.sprite_filepath = sprite_filepath
        self.transfroms = []
        if sprite_surface is not None:
            self.image = sprite_surface
        elif self.sprite_filepath is not None:
            self.load_image()
        else:
            raise SpriteLoadingExecption(
                "Could not load a image data for this sprite")

    # Load the original image.
    def load_image(self):
        try:
            self.image = pygame.image.load(
                os.path.join(self.sprite_filepath)).convert()
        except pygame.error, message:
            raise SpriteLoadingExecption(message)

    # Scale the image, overwrites the original image.
    def scale(self, w, h):
        return Sprite(self.name, init_z=self.z, init_x=self.x, init_y=self.y,
                      sprite_filepath=self.sprite_filepath,
                      sprite_surface=pygame.transform.scale(self.image, (w, h)))

    # Flip the image, overwrites the original image.
    def flip(self, x=False, y=False):
        return Sprite(self.name, init_z=self.z, init_x=self.x, init_y=self.y,
                      sprite_filepath=self.sprite_filepath,
                      sprite_surface=pygame.transform.flip(self.image, x, y))

    # Rotate the image, overwrites the original image.
    def rotate(self, angle=0):
        return Sprite(self.name, init_z=self.z, init_x=self.x, init_y=self.y,
                      sprite_filepath=self.sprite_filepath,
                      sprite_surface=pygame.transform.rotate(self.image, angle))

    # Draw the sprite to the screen
    def draw(self, display):
        display.blit(self.image, (self.x, self.y))


class SpriteLoadingExecption(Exception):
    pass
