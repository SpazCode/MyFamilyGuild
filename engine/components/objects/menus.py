#!/usr/bin/env python
import util
from frames import Frame
from frames import FrameObject
from enum import Enum


# Different Menu Types available.
class MenuType(Enum):
    GRID = 1
    VLIST = 2
    HLIST = 3


# Represents the sizing rule for the menu item.
class MenuItemFillType(Enum):
    FILL = 1
    WRAP = 2


class Menu(Frame):

    def __init__(self, name, init_z=0, init_x=0, init_y=0, init_h=0, init_w=0, 
                 background=None, menu_type=MenuType.GRID, x_padding=5, 
                 y_padding=0, rows=-1, cols=-1):
        # SUPER
        super(Menu, self).__init__(name, init_z, init_x, init_y, init_h, init_w)
        # Define instance variables.
        # Background for the menu.
        self.background = background
        # The current position focused on.
        self.position = (0, 0)
        # The type of menu this is.
        self.type = menu_type
        # The padding for objects in the menu.
        self.x_padding = x_padding
        self.y_padding = y_padding
        # Rows and columns in the menu.
        if menu_type == MenuType.GRID:
            self.rows = rows
            self.cols = cols
        elif menu_type == MenuType.VLIST:
            self.rows = -1
            self.cols = 1
        elif menu_type == MenuType.HLIST:
            self.rows = 1
            self.cols = -1

    # Update the components in the frame.
    def update(self):
        # Clear the surface;
        # self.frame_surface.fill(pygame.Color(0, 0, 0, 255))
        # Sort all components by the z values.
        self.components.sort(key=lambda x: x.z)
        # Run through all the components and update them.
        for component in self.components:
            component.update()
        # Shuffle the items.
        self._format_items()

    # Add new menu item to the menu. Items are added in order and that
    # order determines their placement.
    def add_menu_item(self, item, w, h):
        if util.check_type(item, "DisplayObject"):
            self.components.append(MenuItem(self, item, w, h))
        return self

    # Shuffle the items in the screen the right way.
    def _format_items(self):
        currentItem = 0
        xpos = self.x_padding
        ypos = self.y_padding
        maxh = 0
        while currentItem < len(self.components):
            self.components[currentItem].set_position(xpos, ypos)
            # Determine the max height to move down for the next row.
            maxh = max(maxh, self.components[currentItem].h)
            currentItem += 1
            # Move the item in the menu based on the current item.
            if self.cols > 0 and currentItem % self.cols != 0:
                xpos += self.components[currentItem-1].w + self.xpadding
            else:
                ypos += maxh + self.y_padding


# The container object that is used to define an element in the menu.
class MenuItem(object):

    def __init__(self, menu, content, w, h):
        # Define the parent and content objects.
        self.menu = menu
        self.content = content
        # Determine width dimentions
        if w == MenuItemFillType.FILL:
            self.w = menu.w
        elif w == MenuItemFillType.WRAP:
            self.w = content.w
        else:
            self.w = w
        # Determine height dimentions
        if h == MenuItemFillType.FILL:
            self.h = menu.h
        elif h == MenuItemFillType.WRAP:
            self.h = content.h
        else:
            self.h = h
        # Initialize the screen position.
        self.x = 0
        self.y = 0
        self.z = content.z

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.content.update()

    def draw(self, display):
        self.content.x = self.x
        self.content.y = self.y
        self.content.draw(display)
        self._update_object_abs_position()

    def _update_object_abs_position(self):
        self.content.x = self.x + self.menu.x
        self.content.y = self.y + self.menu.y

