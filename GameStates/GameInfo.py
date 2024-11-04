class GameInfo:
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
        self.has_crib = False
        self.cards_in_play = []
        self.top_card = []
        self.our_hand = []
        self.other_hand = []
        # Integers of player scores
        self.our_score = 0
        self.other_score = 0
        self.crib_score = 0
        # Booleans for determining the State of Game
        self.crib_hidden = True
        self.is_dealer = False
        self.is_turn = False
        self.can_play = False
