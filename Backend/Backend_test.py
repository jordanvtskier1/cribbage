from Backend import Backend
from GameStates.GameInfo import GameInfo
#from Card import Card


game_info = GameInfo()
game_info = Backend.deal_cards(game_info)

assert len(game_info.deck) == 52