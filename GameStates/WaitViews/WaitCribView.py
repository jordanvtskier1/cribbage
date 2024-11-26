# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade

from Backend_test import game_info
from GameStates import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
import arcade.gui
from GameStates.StateTransitionBackend import StateTransitionBackend
from Card import Card
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU


class WaitCribView(GameView):
    """Class representing the adding cards to the crib portion of the game"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.other_picks = []
        self.listener_done = False

        self.crib_location = self.get_crib_location()

        self.tip_string = "Wait for other player's crib picks"


    def on_show(self):
        self.set_our_hand()
        self.set_other_hand()
        self.other_player.listen_to_cribbage(view=self)

    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """

        self.clear()
        self.draw_deck()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()
        self.draw_tips()

        # Animate other cards
        if len(self.other_picks) >= 2:
            self.card_animation(self.other_picks)

        if self.can_transition():
            self.make_transition()

    def can_transition(self):
        if self.listener_done:
            for card in self.other_picks:
                if card.is_animating:
                    return False
            return True
        return False

    def make_transition(self):

        self.transition.wait_crib_transition(
            cards= self.other_picks,
            game_info=self.game_info
        )

    #                   Animations
    # ===================================================#
    def card_animation(self, cards):
        for card in cards:
            card.get_dealt_animation(end_position=self.crib_location)