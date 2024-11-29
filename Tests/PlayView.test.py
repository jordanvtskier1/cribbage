import arcade


from GameStates.GameInfo import GameInfo
from GameStates.MenuViews.MainMenuView import MainMenuView
from GameStates.StateTransitionBackend import StateTransitionBackend
from Backend.BackendFunctions import Backend


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"




"Sets up a hand that allows you to force the other player to play/not play"
def set_up_dynamic_hand(game_info: GameInfo):
    from Card import Card
    game_info.our_hand = [
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
    game_info.top_card = Card(suit="Worms", rank=3)


"you are the dealer"
def set_up_test_one(game_info: GameInfo):

    set_up_dynamic_hand(game_info)
    game_info.is_dealer = True

"you are not the dealer"
def set_up_test_two(game_info: GameInfo):
    set_up_dynamic_hand(game_info)
    game_info.is_dealer = False

def we_start(game_info, state_transition):
    from GameStates.ActiveViews.PlayView import PlayView
    return PlayView(game_info=game_info, state_transition=state_transition)

def other_start(game_info, state_transition):
    from GameStates.WaitViews.WaitPlay import WaitPlayView
    return WaitPlayView(game_info=game_info, state_transition=state_transition)

def main():
    from Adversary.CPU import CPU

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    state_transition = StateTransitionBackend(window)
    game_info = GameInfo()
    game_info.other_player = CPU()
    #set up test
    set_up_test_one(game_info)

    view = we_start(game_info, state_transition)
    window.show_view(view)

    # Run the Window
    arcade.run()

if __name__ == '__main__':
    main()