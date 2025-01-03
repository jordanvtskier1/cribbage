"""
Main file, used to start program
CS 3050: Software Engineering
Final Project: Cribbage Game
"""

import arcade
from GameStates.GameInfo import GameInfo
from GameStates.MenuViews.MainMenuView import MainMenuView
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.PickCardView import PickCardView
from GameStates.AddToCribView import AddToCribView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"


def main():
    # Create game window
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    state_transition = StateTransitionBackend(window)
    game_info = GameInfo()

    menu = AddToCribView(game_info, state_transition)#MainMenuView(game_info=game_info, state_transition=state_transition)
    window.show_view(menu)

    # Run the Window
    arcade.run()


if __name__ == '__main__':
    main()
