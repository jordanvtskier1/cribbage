# A class to handle the State of the Game as well as altering the state
# CS 3050: Software Engineering
#


class Game:

    # NOTE: Feel free to add or alter variables just mention the change in your commit message - Carson
    def __init__(self):
        # List of Card Objects
        self.deck = []
        self.crib = []
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
