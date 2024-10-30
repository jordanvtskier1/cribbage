from Card import Card
from GameStates.GameInfo import GameInfo
import random

class Backend:

    def __init__(self):
        pass

    @staticmethod
    def deal_cards(game_info: GameInfo):
        SUITS = game_info.SUITS
        CARD_VALUES = game_info.CARD_VALUES
        for suit in SUITS: 
            for value in CARD_VALUES: 
                game_info.deck.append(Card(suit, value))
        return random.shuffle(game_info.deck)



