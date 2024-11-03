import arcade
from GUI.Window import Window
from GameStates.GameInfo import GameInfo
from GameStates.PickCardView import PickCardView
from GameStates.AddToCribView import AddToCribView
from GameStates.CutDeckView import CutDeckView
from GameStates.MenuView import MenuView
from GameStates.StateTransitionBackend import StateTransitionBackend

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"


def main():
    # window = Window()
    # window.setup()
    # arcade.run()

    # Creates a window for the cribbage game to be displayed on
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    state_transition = StateTransitionBackend(window)

    # Create a game_state object
    game_info = GameInfo()

    menu = MenuView(game_info=game_info,  state_transition=state_transition)
    window.show_view(menu)

    # pick_card_view = PickCardView(game_info)
    # window.show_view(pick_card_view)

    # add_crib_view = AddToCribView(game_info)
    # window.show_view(add_crib_view)

    # cut_deck_view = CutDeckView(game_info)
    # window.show_view(cut_deck_view)

    # Run the Window
    arcade.run()

if __name__ == '__main__':
    main()