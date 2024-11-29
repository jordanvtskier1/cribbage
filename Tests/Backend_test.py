from Backend.BackendFunctions import Backend
from GameStates.GameInfo import GameInfo
#from Card import Card


game_info = GameInfo()
game_info = Backend.create_deck(game_info)

assert len(game_info.deck) == 52
print("create_deck Passed")

game_info = Backend.deal_cards(game_info)

assert len(game_info.our_hand) == game_info.DEAL
assert len(game_info.other_hand) == game_info.DEAL
print("deal_cards passed")

print("OUR HAND:")
for card in game_info.our_hand:
    print(card)

print("\nOTHER HAND:")
for card in game_info.other_hand:
    print(card)

print("\nDECK:")
for card in game_info.deck:
    print(card)

