#!/usr/bin/env python3
import pygame
import util
from inputs import Inputs

"""
    Scene shown on screen. The Scene manages the drawing of components on
    screen, the order in which they are drawn, and updating the underlying
    logic of the components on screen.
"""


class Scene(object):

    def __init__(self):
        self.screen = None
        self.inputs = Inputs()
        # The list of components in the scene. Components are drawn in order in
        # the list
        self.background = []
        self.foreground = []
        self.midground = []
        # The scene manager that this scene sits in.
        self.manager = None
        # The settings for the game.
        self.settings = None

    # Build the scene components.
    def build(self):
        pass

    # Informs the scene of the screen.
    def set_screen(self, screen):
        self.screen = screen

    # Informs the scene of the game settings.
    def set_settings(self, settings):
        self.settings = settings

    # Add components to a specific layer. Only Display componetns can be added
    # to a Scene.
    def add_component_background(self, component):
        if util.check_type(component, "DisplayObject"):
            self.background.append(component)

    def add_component_midground(self, component):
        if util.check_type(component, "DisplayObject"):
            self.midground.append(component)

    def add_component_foreground(self, component):
        if util.check_type(component, "DisplayObject"):
            self.foreground.append(component)

    def update(self):
        # Update inputs.
        self.inputs.update(pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]))
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


class SceneManager(object):
    def __init__(self):
        self.scenes = {}
        self.current_scene = ""

    def add_scene(self, name, scene):
        if util.check_type(scene, "Scene"):
            scene.manager = self
            self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes.keys():
            self.current_scene = name

    def update(self):
        self.scenes[self.current_scene].update()
        self.scenes[self.current_scene].draw()

    def set_screen(self, screen):
        for key in self.scenes.keys():
            self.scenes[key].set_screen(screen)

    def set_settings(self, settings):
        for key in self.scenes.keys():
            self.scenes[key].set_settings(settings)

    def build_scenes(self):
        for key in self.scenes.keys():
            self.scenes[key].build()
