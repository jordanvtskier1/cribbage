from GameStates.GameInfo import GameInfo
from GameStates.MenuViews.MainMenuView import MainMenuView
from Backend.BackendFunctions import Backend
from Card import Card
import arcade
from GameStates.PickCardView import PickCardView


from GameStates.StateTransitionBackend import StateTransitionBackend
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

state_transition = StateTransitionBackend(window)
game_info = GameInfo()



#state_transition.create_game_to_pick_card(game_info, "kate")


state_transition.join_game_to_pick_card(game_info, "kate")

arcade.run()

#card = game_info.deck[0]

#state_transition.pick_card_to_add_crib(game_info, card)

