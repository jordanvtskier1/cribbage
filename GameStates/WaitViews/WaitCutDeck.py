# View for cutting the deck
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import arcade
from GameStates import GameInfo
from GameStates.CutDeckAnimation import CutDeckAnimation
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.GameView import GameView
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU
import time


class WaitCutDeck(GameView):
    """Class representing the cutting of the deck"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.tip_string = "Wait for your opponent to cut the deck..."
        self.time_one = -1

        self.picked_card = None
        self.listener_done = False
        self.animator = CutDeckAnimation(deck= self.game_info.deck, card = None)

    def on_show(self):
        self.set_other_hand()
        self.set_our_hand()
        self.set_spread_deck()

        if self.game_info.is_multiplayer:
            Multiplayer.listen_to_cut(view=self)
        else:
            CPU.listen_to_cut(view=self)


    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """

        self.clear()

        self.draw_spread_deck()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()

        if not self.game_info.is_dealer:
            self.draw_tips()

        if self.can_transition() and self.animator.play():
            self.make_transition()


    def can_transition(self):
        if self.picked_card is not None:
            if not self.picked_card.is_animating:
                return True
        return False

    def make_transition(self):
        self.transition.wait_cut_to_wait_play(
            game_info=self.game_info,
            card = self.picked_card
        )

    def set_cut_deck(self, card):
        self.picked_card = card
        self.animator.card = card
