#!/usr/bin/env python3
import pygame
from inputs import Inputs

"""
    Scene shown on screen. The Scene manages the drawing of components on
    screen, the order in which they are drawn, and updating the underlying
    logic of the components on screen.
"""


class Scene(object):

    def __init__(self, screen):
        self.screen = screen
        self.inputs = Inputs()
        # The list of components in the scene. Components are drawn in order in
        # the list
        self.background = []
        self.foreground = []
        self.midground = []
        # The scene manager that this scene sits in.
        self.manager = None
        # Build the scene components.
        self.build()

    def build(self):
        pass

    # Add components to a specific layer. Only Display componetns can be added
    # to a Scene.
    def add_component_background(self, component):
        if self.__check_if_display_object(component):
            self.background.append(component)

    def add_component_midground(self, component):
        if self.__check_if_display_object(component):
            self.midground.append(component)

    def add_component_foreground(self, component):
        if self.__check_if_display_object(component):
            self.foreground.append(component)

    def update(self):
        # Update inputs.
        self.inputs.update(pygame.event.get())
        # Update the game components.
        for component in self.background + self.midground + self.foreground:
            component.update()
        # Re-Shuffle each layer of components.
        self.background.sort(key=lambda x: x.z)
        self.midground.sort(key=lambda x: x.z)
        self.foreground.sort(key=lambda x: x.z)

    def draw(self):
        # Draw background components.
        for component in self.background:
            component.draw(self.screen.get_display())

        # Draw middle ground components.
        for component in self.midground:
            component.draw(self.screen.get_display())

        # Draw foreground components.
        for component in self.foreground:
            component.draw(self.screen.get_display())

    def __check_if_display_object(self, obj):
        if type(obj).__name__ == "DisplayObject":
            return True
        for classes in type(obj).__bases__:
            if classes.__name__ == "DisplayObject":
                return True
        return False


class SceneManager(object):
    def __init__(self):
        self.scenes = {}
        self.current_scene = ""

    def add_scene(self, name, scene):
        if self.__check_if_scene(scene):
            scene.manager = self
            self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes.keys():
            self.current_scene = name

    def update(self):
        self.scenes[self.current_scene].update()
        self.scenes[self.current_scene].draw()

    def __check_if_scene(self, obj):
        if type(obj).__name__ == "Scene":
            return True
        for classes in type(obj).__bases__:
            if classes.__name__ == "Scene":
                return True
        return False

