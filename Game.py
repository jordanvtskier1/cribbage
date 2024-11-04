# A class to handle the State of the Game as well as altering the state
# CS 3050: Software Engineering
#
import arcade
import random
from Card import Card
from GameStates.GameInfo import GameInfo


class Game:
    MAX_PEGGING = 121
    DEAL = 6
    HAND = 4
    POINTS = 15
    MAX_TOTAL = 31
    SUITS = ["Clubs", "Worms", "Diamonds", "Hearts"]
    CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

    def __init__(self):
        pass
        

    @classmethod
    def create_deck(cls, game_info: GameInfo):
        from GUI.CardSpriteResolver import CardSpriteResolver
        game_info.reset()

        for suit in cls.SUITS:
            for value in cls.CARD_VALUES:
                game_info.deck.append(Card(suit, value))
        random.shuffle(game_info.deck)
        return
    
    @classmethod
    def deal_hands(cls, game_info: GameInfo):
        for index in range(0, (cls.DEAL*2), 2):
            game_info.our_hand.append(game_info.deck[index])
            game_info.other_hand.append(game_info.deck[index + 1])
        return

    @classmethod
    def card_played(cls, hand_index, game_info: GameInfo):
        game_info.cards_in_play.append(game_info.our_hand[hand_index])
        game_info.our_hand.pop(hand_index)

    @classmethod
    def send_to_crib(cls, cards, game_info: GameInfo):

        # This popped a card and then used an index which was not valid any more
        # if len(hand_indexes) != 2:
        #     raise Exception("Must send 2 cards to the crib")
        # for hand_index in hand_indexes:
        #     game_info.crib.append(game_info.our_hand[hand_index])
        #     game_info.our_hand.pop(hand_index)

        if len(cards) != 2:
            raise Exception("Must send 2 cards to the crib")
        for card in cards:
            game_info.crib.append(card)
            game_info.our_hand.remove(card)


    # My idea for how multiplayer will work
    # This function will get called whenever it is the opponent's turn
    def get_player2_moves(self):
        pass
        # wait for firebase to change
        # retrieve firebase data
        # set player2, crib, deck 
        


    

        