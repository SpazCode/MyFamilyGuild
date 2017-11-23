#!/usr/bin/env python3


# Class to represent game objects on screen. Display objects
# have screen position, colition detection and are labled with a name.
class DisplayObject(object):

    # Constructor
    def __init__(self, name, init_x=0, init_y=0, init_h=0, init_w=0):
        self.name = name
        self.x = init_x
        self.y = init_y
        self.w = init_w
        self.h = init_h

    # Check if object has collided
    def collided(self, obj):
        if (self.x >= obj.x and self.x < obj.x + obj.w) or (self.x + self.w > obj.x and self.x + self.w < obj.x + obj.w):
            if (self.y >= obj.y and self.y < obj.y + obj.h) or (self.y + self.h > obj.y and self.y + self.h < obj.y + obj.h):
                return True

    # Deterine the center of the Object
    # returns a tuple (cx, cy).
    def get_center(self):
        cx = self.x+(self.w/2)
        cy = self.y+(self.h/2)
        return (cx, cy)

    # Draw the display object to screen.
    def draw(self, display):
        pass

    # Update game everyframe.
    def update(self):
        pass

    # String representation of the DOsplay Object on screen.
    def __str__(self):
        return "{0}: [x: {1}, y: {2}, w: {3}, h: {4}]".format(
            self.name, self.x, self.y, self.w, self.h)
