# A class to handle the State of the Game as well as altering the state
# CS 3050: Software Engineering
#
import arcade
import random
from Card import Card


class Game:
    MAX_PEGGING = 121
    DEAL = 6 
    HAND = 4
    POINTS = 15
    MAX_TOTAL = 31
    SUITS = ["Clubs", "Spades", "Diamonds", "Hearts"]
    CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

    # NOTE: Feel free to add or alter variables just mention the change in your commit message - Carson
    def __init__(self):
        # List of Card Objects
        self.deck = []
        self.crib = []
        self.cards_in_play = []
        self.player1_hand = []
        self.player2_hand = []
        # Integers of player scores
        self.player1_score = 0
        self.player2_score = 0
        # Booleans for determining the State of Game
        self.crib_hidden = True
        self.player1_dealer = True
        self.player1_turn = True
        self.is_player1 = True

    def create_deck(self, SUITS, CARD_VALUES): 
        for suit in SUITS: 
            for value in CARD_VALUES: 
                self.deck.append(Card(suit, value))
        return random.shuffle(self.deck)
    
    
    def deal_hands(self, DEAL): 
        for index in range(0, (DEAL*2), 2):
            self.player1_hand.append(self.deck[index])
            self.player2_hand.append(self.deck[index + 1])
        return self.player1_hand, self.player2_hand
    
    def card_played(self, hand_index):
        self.cards_in_play.append(self.player1_hand[hand_index])
        self.player1_hand.pop(hand_index)

    def send_to_crib(self, hand_index):
        
        if len(hand_index) != 2:
            raise Exception("Must send 2 cards to the crib")
        self.crib.append(self.player1_hand[hand_index])
        self.player1_hand.pop(hand_index)


    # My idea for how multiplayer will work
    # This function will get called whenever it is the opponent's turn
    def get_player2_moves(self):
        pass
        # wait for firebase to change
        # retrieve firebase data
        # set player2, crib, deck 
        


    

        