import arcade


from GameStates.GameInfo import GameInfo
from GameStates.MenuViews.MainMenuView import MainMenuView
from GameStates.StateTransitionBackend import StateTransitionBackend
from Backend.BackendFunctions import Backend

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"


def set_up_test(game_info: GameInfo):
    from Card import Card
    game_info.our_hand = [
        Card(
            suit = "Worms",
            rank = "K"
        ),
        Card(
            suit="Worms",
            rank="K"
        ),
        Card(
            suit="Worms",
            rank=2
        ),
        Card(
            suit="Worms",
            rank="A"
        )
    ]

    game_info.other_hand = [
        Card(
            suit="Worms",
            rank="K"
        ),
        Card(
            suit="Worms",
            rank="K"
        ),
        Card(
            suit="Worms",
            rank="K"
        ),
        Card(
            suit="Worms",
            rank="K"
        )
    ]


def main():
    from Adversary.CPU import CPU
    from GameStates.ActiveViews.PlayView import PlayView
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    state_transition = StateTransitionBackend(window)
    game_info = GameInfo()
    game_info.other_player = CPU()
    #set up test
    set_up_test(game_info)

    view = PlayView(game_info=game_info, state_transition=state_transition)
    window.show_view(view)

    # Run the Window
    arcade.run()

if __name__ == '__main__':
    main()