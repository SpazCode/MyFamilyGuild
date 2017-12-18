#!/usr/bin/env python3
import pygame


class Inputs(object):
    # Inner Class to allow for disabling a keymapping.

    class Input(object):
        # Constructor.

        def __init__(self, c):
            self.enabled = True
            self.callback = c

        # Run the callback.
        def run(self):
            if self.enabled:
                self.callback()

    # Constrictor,
    def __init__(self):
        self.___key_mapping = {}

    # Add new key binding,
    def set(self, key, callback):
        self.___key_mapping[key] = self.Input(callback)

    # Disable key binding.
    def enabled(self, key, status=True):
        self.___key_mapping[key].enabled = status

    # Run the key presses.
    def update(self, events):
        for event in events:
            k = Inputs.CreateInputKey(event.type, event.key)
            if k in self.___key_mapping.keys():
                self.___key_mapping[k].run()

    # Output of inputs.
    def __str__(self):
        return str(self.___key_mapping)

    @staticmethod
    def CreateInputKey(_type, key):
        return "{0}_{1}".format(_type, key)
