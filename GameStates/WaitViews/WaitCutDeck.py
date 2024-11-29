# View for cutting the deck
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import arcade
from GameStates import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.GameView import GameView
from GameStates.CutDeckAnimation import CutDeckAnimation
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU
import time


class WaitCutDeck(GameView):
    """Class representing the cutting of the deck"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.tip_string = "Wait for your opponent to cut the deck..."
        self.time_one = -1

        self.tip_message = arcade.gui.UILayout(
                x=self.GUIDE_LOCATION[0],
                y=self.GUIDE_LOCATION[1],
            children = [arcade.gui.UIMessageBox(
                width=400,
                height=35,
                message_text = self.tip_string,
                buttons=[]
            )]
            )
        self.manager.add(
            self.tip_message
        )

        self.picked_card = None
        self.listener_done = False
        self.animator = CutDeckAnimation(deck= self.game_info.deck, card = None)

    def on_show(self):
        self.set_other_hand()
        self.set_our_hand()
        self.set_spread_deck()

        self.other_player.listen_to_cut(view = self)


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
        self.manager.draw()

        is_done_animating = self.animator.play()
        if self.can_transition() and is_done_animating:
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
