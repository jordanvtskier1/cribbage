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
        game_info.deck = random.shuffle(game_info.deck)
        return game_info
    
    def add_to_crib(game_info: GameInfo, card1: Card, card2: Card):
        game_info.crib.append(card1)
        game_info.crib.append(card2)
        game_info.our_hand.remove(card1)
        game_info.our_hand.remove(card2)
        return game_info





