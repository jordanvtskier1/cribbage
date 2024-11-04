from Card import Card
class GameInfo:
    MAX_PEGGING = 121
    DEAL = 6
    HAND = 4
    POINTS = 15
    MAX_TOTAL = 31
    SUITS = ["Clubs", "Worms", "Diamonds", "Hearts"]
    CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

    # NOTE: Feel free to add or alter variables just mention the change in your commit message - Carson
    def __init__(self):
        # List of Card Objects
        self.deck = []
        self.crib = []
        self.has_crib = False
        self.cards_in_play = []
        self.our_hand = []
        self.other_hand = []
        # self.our_hand = [Card("1",""),Card("2",""),Card("3",""),Card("4",""),Card("5",""),Card("6","")]
        # self.other_hand = [Card("1",""),Card("2",""),Card("3",""),Card("4",""),Card("5",""),Card("6","")]
        # Integers of player scores
        self.our_score = 0
        self.other_score = 0
        # Booleans for determining the State of Game
        self.crib_hidden = True
        self.is_dealer = True
        self.is_turn = True
        self.can_play = False

    def reset(self):
        self.deck = []
        self.cards_in_play = []
        self.our_hand = []
        self.other_hand = []

