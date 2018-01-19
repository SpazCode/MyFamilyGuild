#!/usr/bin/python3
import pygame
import util
from display_object import DisplayObject


class Frame(DisplayObject):
    # Constructor
    def __init__(self, name, init_z=0, init_x=0, init_y=0, init_h=0, init_w=0):
        # SUPER
        super(Frame, self).__init__(name, init_z, init_x, init_y, init_h, init_w, 0, 0)
        # Create the surface for the frame.
        self.frame_surface = pygame.Surface(self.get_size(), pygame.SRCALPHA, 32).convert_alpha()
        # Background image/surface.
        self.background = None
        # List of components in the frame.
        self.components = []

    # Update the components in the frame.
    def update(self):
        # Clear the surface;
        # self.frame_surface.fill(pygame.Color(0, 0, 0, 255))
        # Sort all components by the z values.
        self.components.sort(key=lambda x: x.z)
        # Run through all the components and update them.
        for component in self.components:
            component.update()

    # Draw the frame.
    def draw(self, display):
        # Place the background to fill the surface.
        if self.background is not None:
            if util.check_type(self.background, "Color"):
                self.frame_surface.fill(self.background)
            elif util.check_type(self.background, "Sprite"):
                self.background.scale(self.w, self.h)
                self.frame_surface.blit(self.background, (0, 0))
        # Draw each component in order.
        for component in self.components:
            component.draw(self.frame_surface)
        # Draw the frame to the screen.
        display.blit(self.frame_surface, (self.x, self.y))

    # Adds a component to the frame.
    def add_components(self, component, x, y):
        if util.check_type(component, "DisplayObject"):
            self.components.append(FrameObject(component, self, x, y))
        return self


# The container for objects in a frame. Tracks the relative position of the object in the frame.
class FrameObject(object):

    def __init__(self, obj, frame, x, y):
        self.frame = frame
        self.object = obj
        self.z = self.object.z
        self.x = x
        self.y = y
        self.update_object_abs_position()

    def update(self):
        self.object.update()

    def draw(self, display):
        self.object.x = self.x
        self.object.y = self.y
        self.object.draw(display)
        self.update_object_abs_position()

    def update_object_abs_position(self):
        self.object.x = self.x + self.frame.x
        self.object.y = self.y + self.frame.y
