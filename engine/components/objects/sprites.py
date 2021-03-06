#!/usr/bin/env python3
import os

import pygame
import util

from display_object import DisplayObject


class Sprite(DisplayObject):
    def __init__(self, name, init_z=0, init_x=0, init_y=0,
                 init_ox=0, init_oy=0, sprite_surface=None,
                 sprite_filepath=None):
        super(Sprite, self).__init__(
            name, init_z, init_x, init_y, 0, 0, init_ox, init_oy)
        self.image = None
        self.sprite_filepath = sprite_filepath
        if sprite_surface is not None:
            self.image = sprite_surface
        elif self.sprite_filepath is not None:
            self.load_image()
        else:
            raise SpriteLoadingExecption(
                "Could not load a image data for this sprite")
        self.w = self.image.get_width()
        self.h = self.image.get_height()

    # Load the original image.
    def load_image(self):
        try:
            self.image = pygame.image.load(
                os.path.join(self.sprite_filepath)).convert_alpha()
        except pygame.error, message:
            raise SpriteLoadingExecption(message)

    # Scale the image, overwrites the original image.
    def scale(self, w, h):
        self.set_origin(self.originx * w / self.w, self.originy * h / self.h)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.w = self.image.get_width()
        self.h = self.image.get_height()
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
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            raise SpriteLoadingExecption(message)

    def get_sprite(self, name, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return Sprite(name, sprite_surface=image)

    def get_sprites(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]


# Object to represent set of frames for an animation.
class FrameData(object):
    def __init__(self, _dict):
        self.frames = {}
        vars(self).update(_dict)
        for key in self.frames.keys():
            self.frames[key] = Frame(self.frames[key])


# Data Object to represent a single frame in an animation.
class Frame(object):
    def __init__(self, _dict):
        vars(self).update(_dict)


class SpriteAnimation(DisplayObject):
    def __init__(self, name, init_z=0, init_x=0, init_y=0,
                 init_ox=0, init_oy=0, sprite_sheet=None,
                 frame_data=None, loop=True):
        # SUPER CALL
        super(SpriteAnimation, self).__init__(
            name, init_z, init_x, init_y, 0, 0, init_ox, init_oy)
        # Throw exception if there is no framedata or spritesheet.
        if frame_data is None or sprite_sheet is None:
            raise InvalidArgumentsExecption(
                "No Sprite Sheet or Frame Data has been loaded")
        # Ensure that the spritesheet is class SpriteSheetManager.
        if util.check_type(sprite_sheet, "SpriteSheetManager"):
            self.sprite_sheet = sprite_sheet
        # Ensure that the framedata is class FrameData.
        if util.check_type(frame_data, "FrameData"):
            self.frame_data = frame_data
        # Callback for when the animation completes.
        self.finish_callback = None
        # The total frame length of the animation.
        self.anim_length = sum(self.frame_data.waits)
        # The current frame that the animation is on.
        self.curr_anim_time = 0
        # The index in the frame order.
        self.curr_sprite = 0
        # The next point in animation time to incrament the order index.
        self.next_incrament = 0
        # Flag for playing the animation.
        self.play = True
        # Flag for looping the animation.
        self.loop = loop
        # Load animation based on framedata.
        self.load_animation()

    def scale(self, w_scale=1, h_scale=1):
        for key in self.frame_data.frames.keys():
            w = self.frame_data.frames[key].w * w_scale
            h = self.frame_data.frames[key].h * h_scale
            self.frame_data.frames[key].sprite.scale(w, h)
        return self

    def flip(self, x=False, y=False):
        self.flipx = x
        self.flipy = y
        for key in self.frame_data.frames.keys():
            self.frame_data.frames[key].sprite.flip(x=self.flipx, y=self.flipy)
        return self

    def rotate(self, angle=0):
        self.angle = angle
        for key in self.frame_data.frames.keys():
            self.frame_data.frames[key].sprite.rotate(angle=angle)
        return self

    # Load the sprites of the animation.
    def load_animation(self):
        for key in self.frame_data.frames.keys():
            self.frame_data.frames[key].sprite = self.sprite_sheet.get_sprite(key,
                                                                              (self.frame_data.frames[key].x,
                                                                               self.frame_data.frames[key].y,
                                                                               self.frame_data.frames[key].w,
                                                                               self.frame_data.frames[key].h),
                                                                              self.frame_data.frames[key].a)
            self.frame_data.frames[key].sprite.set_origin(self.frame_data.frames[key].ox,
                                                          self.frame_data.frames[key].oy)
        self.next_incrament += self.frame_data.waits[self.curr_sprite]

    # Move animation based on the sprites origin.
    def move_to(self, x, y):
        self.x = x
        self.y = y
        return self

    # Toogle if the animation is played.
    def toggle_play(self):
        self.play = not self.play
        return self

    # Toogle if the animation is looped.
    def toggle_loop(self):
        self.loop = not self.loop
        return self

    # Reset the animations.
    def reset(self):
        self.curr_sprite = 0
        self.curr_anim_time = 0
        self.next_incrament = 0 + self.frame_data.waits[self.curr_sprite]
        return self

    # Update the Sprite based on the place in the animation.
    def update(self):
        if self.play:
            # Incrament animation time.
            self.curr_anim_time += 1
            if self.curr_anim_time >= self.anim_length:
                if self.finish_callback is not None:
                    self.finish_callback()
                    return
                elif self.loop:
                    self.reset()
                else:
                    self.toggle_play()
                    return

            # Decide what sprite to show.
            if self.curr_anim_time >= self.next_incrament:
                self.curr_sprite += 1
                self.next_incrament += self.frame_data.waits[self.curr_sprite]

            # Update sprites position.
            self.frame_data.frames[self.frame_data.order[
                self.curr_sprite]].sprite.move_to(self.x, self.y)

    # Draw the animation.
    def draw(self, display):
        # Update the location again just to make sure it is at the right spot.
        self.frame_data.frames[self.frame_data.order[
            self.curr_sprite]].sprite.move_to(self.x, self.y)
        # Draw the current sprite.
        self.frame_data.frames[self.frame_data.order[
            self.curr_sprite]].sprite.draw(display)


# A set of sprite animations.
# Easy way to load muliple sprite animations and defining keys between them.
class SpriteAnimationSet(DisplayObject):
    # Consturctor
    def __init__(self, name, init_z=0, init_x=0, init_y=0,
                 init_ox=0, init_oy=0, animations=[]):
        # SUPER CALL
        super(SpriteAnimationSet, self).__init__(
            name, init_z, init_x, init_y, 0, 0, init_ox, init_oy)
        if len(animations) <= 0:
            raise InvalidArgumentsExecption("No animation files set.")
        # Loads animations framedata and spritesheets.
        self.animations = {}
        spritesheet = {}
        for animation in animations:
            framedata = FrameData(util.load_json(animation[1]))
            if framedata.sprite_sheet not in spritesheet.keys():
                spritesheet[framedata.sprite_sheet] = SpriteSheetManager(
                    framedata.sprite_sheet)
            self.animations[animation[0]] = SpriteAnimation(animation[0], init_z=1, init_x=0,
                                                            init_y=0, frame_data=framedata,
                                                            sprite_sheet=spritesheet[framedata.sprite_sheet])
        self.curr_animation = animations[0][0]

    # Set the current animation.
    def set_animation(self, anim):
        if anim not in self.animations.keys():
            raise InvalidArgumentsExecption(anim + " is not in the animation set.")
        self.curr_animation = anim
        self.animations[anim].reset()
        self.animations[anim].move_to(self.x, self.y)
        self.animations[anim].play = True

    # Set animation onFinishCallbacks
    def set_on_finish(self, key, callback):
        if key not in self.animations.keys():
            raise InvalidArgumentsExecption(key + " is not in the animation set.")
        self.animations[key].finish_callback = callback

    # Move the animations to a position on screen based on their origins.
    def move_to(self, x, y):
        self.x = x
        self.y = y
        return self

    # Scale an animation.
    def scale(self, anim=None, w_scale=1, h_scale=1):
        if anim is None:
            for key in self.animations.keys():
                self.animations[key].scale(w_scale=w_scale, h_scale=h_scale)
        else:
            self.animations[anim].scale(w_scale=w_scale, h_scale=h_scale)
        return self

    # Flip an animation.
    def flip(self, anim=None, x=False, y=False):
        if anim is None:
            for key in self.animations.keys():
                self.animations[key].flip(x=x, y=y)
        else:
            self.animations[anim].flip(x=x, y=y)
        return self

    # Rotate an animation.
    def roate(self, anim=None, angle=0):
        if anim is None:
            for key in self.animations.keys():
                self.animations[key].rotate(angle=angle)
        else:
            self.animations[anim].rotate(angle=angle)
        return self

    # Update the current animation.
    def update(self):
        self.animations[self.curr_animation].move_to(self.x, self.y)
        self.animations[self.curr_animation].update()

    # Draw the current animation.
    def draw(self, display):
        self.animations[self.curr_animation].draw(display)


# Exceptions for sprites.
class SpriteLoadingExecption(Exception):
    pass


# Exception for invalid arguments
class InvalidArgumentsExecption(Exception):
    pass
