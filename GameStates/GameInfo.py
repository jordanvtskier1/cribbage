from Card import Card
from Adversary.OtherPlayerLogic import OtherPlayerLogic

class GameInfo:
    MAX_PEGGING = 121
    DEAL = 6
    HAND = 4
    POINTS = 15
    MAX_TOTAL = 31
    MAX_PLAYABLE_CARDS = 8
    SUITS = ["Clubs", "Worms", "Diamonds", "Hearts"]
    CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

    # NOTE: Feel free to add or alter variables just mention the change in your commit message - Carson
    def __init__(self):
        # List of Card Objects
        self.deck = []
        self.crib = []
        self.has_crib = False
        self.cards_in_play = []
        #Once we go over 31, we store cards in play here
        self.cards_played = []
        self.top_card = None
        self.our_hand = []
        self.other_hand = []
        self.current_count = 0
        # self.our_hand = [Card("1",""),Card("2",""),Card("3",""),Card("4",""),Card("5",""),Card("6","")]
        # self.other_hand = [Card("1",""),Card("2",""),Card("3",""),Card("4",""),Card("5",""),Card("6","")]
        # Integers of player scores
        self.our_score = 0
        self.other_score = 0
        self.crib_score = 0
        self.our_hand_score = 0
        self.other_hand_score = 0
        # Booleans for determining the State of Game
        self.our_win = False
        self.other_win = False
        self.crib_hidden = True
        self.is_dealer = False
        self.is_turn = True
        self.can_play = False
        self.opponent = "player2"
        self.player = "player1"
        self.is_multiplayer = False
        self.other_player = OtherPlayerLogic()

    def reset(self):
        self.deck = []
        self.crib = []
        self.cards_in_play = []
        self.our_hand = []
        self.other_hand = []
        self.current_count = 0

        self.top_card = None

    def count_cards_played(self):
        sum = 0
        for set in self.cards_played:
            sum += len(set)
        sum += len(self.cards_in_play)
        return sum

