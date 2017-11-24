#!/usr/bin/env python3
from engine.game import Game

if __name__ == "__main__":
    game = Game("settings.json")
    game.run_game()
