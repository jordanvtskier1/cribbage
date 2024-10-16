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
    SUITS = ["Ace", "Spades", "Diamonds", "Hearts"]
    CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]

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

    def deck(self, SUITS, CARD_VALUES): 
        for suit in SUITS: 
            for value in CARD_VALUES: 
                self.deck.append((value, suit))
        return random.shuffle(self.deck)
    
    def deal(self, DEAL): 
        for index in range(0, (DEAL*2), 2):
            self.player1_hand.append(self.deck[index])
            self.player2_hand.append(self.deck[index + 1])
        return self.player1_hand, self.player2_hand

        