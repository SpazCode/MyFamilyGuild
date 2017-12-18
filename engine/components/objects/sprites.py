#!/usr/bin/env python3
import os
import pygame
import util
from display_object import DisplayObject


class Sprite(DisplayObject):

    def __init__(self, name, init_z=0, init_x=0, init_y=0,
                 init_ox=0, init_oy=0, sprite_surface=None,
                 sprite_filepath=None, sprite_transparent=False):
        super(Sprite, self).__init__(
            name, init_z, init_x, init_y, 0, 0, init_ox, init_oy)
        self.image = None
        self.sprite_filepath = None
        self.sprite_filepath = sprite_filepath
        self.transfroms = []
        if sprite_surface is not None:
            self.image = sprite_surface
        elif self.sprite_filepath is not None:
            self.load_image(sprite_transparent)
        else:
            raise SpriteLoadingExecption(
                "Could not load a image data for this sprite")

    # Load the original image.
    def load_image(self, transparent):
        try:
            if not transparent:
                self.image = pygame.image.load(
                    os.path.join(self.sprite_filepath)).convert()
            else:
                self.image = pygame.image.load(
                    os.path.join(self.sprite_filepath)).convert_alpha()
            self.w = self.image.get_width()
            self.h = self.image.get_height()
        except pygame.error, message:
            raise SpriteLoadingExecption(message)

    # Scale the image, overwrites the original image.
    def scale(self, w, h):
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(self.image, (w, h))
        return self

    # Flip the image, overwrites the original image.
    def flip(self, x=False, y=False):
        self.flipx = x
        self.flipy = y
        self.image = pygame.transform.flip(self.image, x, y)
        return self

    # Rotate the image, overwrites the original image.
    def rotate(self, angle=0):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, angle)
        return self

    # Draw the sprite to the screen
    def draw(self, display):
        display.blit(self.image, (self.x, self.y))


class SpriteSheetManager(object):

    def __init__(self, filename, transparent=False):
        self.transparent = transparent
        try:
            if not transparent:
                self.sheet = pygame.image.load(filename).convert()
            else:
                self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            raise SpriteLoadingExecption(message)

    def get_sprite(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        if not self.transparent:
            image = pygame.Surface(rect.size).convert()
        else:
            image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return Sprite("", sprite_surface=image)

    def get_sprites(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]


class SpriteAnimation(DisplayObject):

    def __init__(self, name, init_z=0, init_x=0, init_y=0,
                 init_ox=0, init_oy=0, sprite_sheet=None,
                 frame_data=None, loop=True):
        super(SpriteAnimation, self).__init__(
            name, init_z, init_x, init_y, 0, 0, init_ox, init_oy)
        if frame_data is None or sprite_sheet is None:
            raise InvalidArgumentsExecption(
                "No Sprite Sheet or Frame Data has been loaded")
        if util.check_type(sprite_sheet, "SpriteSheetManager"):
            self.sprite_sheet = sprite_sheet
        if util.check_type(frame_data, "FrameData"):
            self.frame_data = frame_data
        self.anim_length = sum(self.frame_data.waits)
        self.curr_anim_time = 0
        self.curr_sprite = 0
        self.next_incrament = 0
        self.play = True
        self.loop = loop
        self.load_animation()

    def scale(self, w_multi=1, h_multi=1):
        for key in self.frame_data.frames.keys():
            w = self.frame_data.frames[key].w * w_multi
            h = self.frame_data.frames[key].h * h_multi
            self.frame_data.frames[key].sprite.scale(w, h)
        return self

    def flip(self, x=False, y=False):
        self.flipx = x
        self.flipy = y
        for key in self.frame_data.frames.keys():
            self.frame_data.frames[key].sprite.flip(x=self.flipx, y=self.flipy)
        return self

    def flip(self, angle=0):
        self.angle = angle
        for key in self.frame_data.frames.keys():
            self.frame_data.frames[key].sprite.rotate(angle=angle)
        return self

    def load_animation(self):
        for key in self.frame_data.frames.keys():
            self.frame_data.frames[key].sprite = self.sprite_sheet.get_sprite((self.frame_data.frames[key].x,
                                                                               self.frame_data.frames[key].y,
                                                                               self.frame_data.frames[key].w,
                                                                               self.frame_data.frames[key].h),
                                                                              self.frame_data.frames[key].a)
        self.next_incrament += self.frame_data.waits[self.curr_sprite]

    def toggle_play(self):
        self.play = not self.play

    def update(self):
        if self.play:
            # Incrament animation time.
            self.curr_anim_time += 1
            if self.curr_anim_time >= self.anim_length:
                if self.loop:
                    self.curr_sprite = 0
                    self.curr_anim_time = 0
                    self.next_incrament = 0 + \
                        self.frame_data.waits[self.curr_sprite]
                else:
                    self.toggle_play()

            # Decide what sprite to show.
            if self.curr_anim_time >= self.next_incrament:
                self.curr_sprite += 1
                self.next_incrament += self.frame_data.waits[self.curr_sprite]

            # Update sprites position.
            self.frame_data.frames[self.frame_data.order[
                self.curr_sprite]].sprite.x = self.x
            self.frame_data.frames[self.frame_data.order[
                self.curr_sprite]].sprite.y = self.y

    def draw(self, display):
        # Draw the current sprite.
        self.frame_data.frames[self.frame_data.order[
            self.curr_sprite]].sprite.draw(display)


class FrameData(object):

    def __init__(self, _dict):
        self.frames = {}
        vars(self).update(_dict)
        for key in self.frames.keys():
            self.frames[key] = Frame(self.frames[key])


class Frame(object):

    def __init__(self, _dict):
        vars(self).update(_dict)


class SpriteLoadingExecption(Exception):
    pass


class InvalidArgumentsExecption(Exception):
    pass
