class CutDeckAnimation:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 650
    CENTER_CARD_LOCATION = [(SCREEN_WIDTH // 4) + 50, SCREEN_HEIGHT / 2]
    DECK_LOCATION = [50, SCREEN_HEIGHT / 2]

    def __init__(self , deck, card):
        self.completed = [ False, False, False]
        self.animations = [ self.cut_deck_animation_first, self.cut_deck_animation_second, self.cut_animation_third]
        self.deck = deck
        self.card = card

    def play(self):
        if self.card is None:
            return False
        for i in range(len(self.animations)):
            if not self.completed[i]:
                self.animations[i]()
                return False
        return True


    def get_last_pos_spread_deck(self):

        card_spacer = len(self.deck) * 10
        return [self.CENTER_CARD_LOCATION[0] - 100 + card_spacer, self.CENTER_CARD_LOCATION[1]]


    def cut_deck_animation_first(self):
        separator_index = self.deck.index(self.card)

        self.card.reveal_card()

        # We separate the left from the right
        left_end_pos = self.DECK_LOCATION
        right_end_pos = self.get_last_pos_spread_deck()
        for deck_index in range(0, separator_index):
            self.deck[deck_index].move_card( end_position= left_end_pos)

        for deck_index in range(separator_index, len(self.deck)):
            self.deck[deck_index].move_card(end_position=right_end_pos)

        for card in self.deck:
            if card.is_animating:
                return
        self.completed[0] = True

    def cut_deck_animation_second(self):

        separator_index = self.deck.index(self.card)
        left_end_pos = self.DECK_LOCATION

        for deck_index in range(separator_index, len(self.deck)):
            self.deck[deck_index].move_card(end_position=left_end_pos)
        self.completed[1] = True

    def cut_animation_third(self):
        for card in self.deck:
            if card is not self.card:
                card.hide_card()
        self.completed[2] = True