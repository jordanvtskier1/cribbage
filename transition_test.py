import arcade
from GameStates.GameInfo import GameInfo
from GameStates.MenuView import MenuView
from GameStates.StateTransitionBackend import StateTransitionBackend


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
state_transition = StateTransitionBackend(window)
game_info = GameInfo()

state_transition.create_game_to_pick_card(game_info, "Kate")



#state_transition.join_game_to_pick_card(game_info, "Kate")



