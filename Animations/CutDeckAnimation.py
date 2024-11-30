from Animations.Animation import Animation
from Animations.AnimationStep import AnimationStep
from Backend.BackendFunctions import Backend
class CutDeckAnimation (Animation):

    def __init__(self , deck, card):
        super().__init__()

        self.completed = False
        self.deck = deck
        self.card = card

        self.animation_steps = [
            AnimationStep(
                duration=999,
                behavior= self.cut_deck_animation_first,
            ),
            AnimationStep(
                duration=999,
                behavior=self.cut_deck_animation_second,
            ),
            AnimationStep(
                duration=999,
                behavior=self.cut_deck_animation_third,
            )
        ]

    def play(self):
        if self.completed or self.card is None:
            return
        for animation_step in self.animation_steps:
            if not animation_step.completed:
                animation_step.play()
                return
        self.completed = True


    def get_last_pos_spread_deck(self):

        card_spacer = len(self.deck) * 10
        return [self.CENTER_CARD_LOCATION[0] - 100 + card_spacer, self.CENTER_CARD_LOCATION[1]]


    def cut_deck_animation_first(self):
        separator_index =  Backend.find_card_in_deck(self.deck, self.card)

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
                return False
        return True

    def cut_deck_animation_second(self):

        separator_index = Backend.find_card_in_deck(self.deck, self.card)
        left_end_pos = self.DECK_LOCATION

        for deck_index in range(separator_index, len(self.deck)):
            self.deck[deck_index].move_card(end_position=left_end_pos)


        for card in self.deck:
            if card.is_animating:
                return False
        return True

    def cut_deck_animation_third(self):
        for card in self.deck:
            if card is not self.card:
                card.hide_card()
        return True