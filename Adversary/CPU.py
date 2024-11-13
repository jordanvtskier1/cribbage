from Adversary.OtherPlayerLogic import OtherPlayerLogic
from GameStates.GameInfo import GameInfo
import random

class CPU(OtherPlayerLogic):
    def __init__(self):
        super().__init__()

    # picks card from deck
    def pick_card(self, game_info: GameInfo):
        deck_size = len( game_info.deck )

        card_index = random.randint(0, deck_size - 1)

        card = game_info.deck[card_index]
        return card

    def add_to_cribbage(self, game_info: GameInfo):
        card_indexes = [
            random.randint(0, len(game_info.other_hand)-1),
            random.randint(0, len(game_info.other_hand)-2)
        ]
        # I know its ugly im sorry
        if card_indexes[0] == card_indexes[1]:
            card_indexes[1] = (card_indexes[1] + random.randint(1, 3)) % 4
        return [game_info.other_hand[card_indexes[0]], game_info.other_hand[card_indexes[1]]]

    def cut_deck(self, game_info: GameInfo):
        deck_size = len(game_info.deck)

        card_index = random.randint(0, deck_size - 1)

        card = game_info.deck[card_index]
        return card

    def play_card(self, game_info: GameInfo):
        card_index = random.randint(0, len(game_info.other_hand) - 1)
        card = game_info.other_hand[card_index]

        return card