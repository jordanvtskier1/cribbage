# View for cutting the deck
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import arcade

from Adversary.Multiplayer import Multiplayer
from GameStates import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.GameView import GameView
import time


class CutDeckView(GameView):
    """Class representing the cutting of the deck"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.tip_string = "Pick a card to cut the deck"
        self.time_one = -1
        self.picked_card = None


    def on_show(self):
        self.set_other_hand()
        self.set_our_hand()
        self.set_spread_deck()

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

        if self.can_transition():
            self.make_transition()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks.
        Clicking a card to cut the deck
        """

        # if self.game_info.is_turn and not self.game_info.is_dealer:
        # Get card object sprites
        card_sprites = arcade.SpriteList()
        for card in self.game_info.deck:
            card_sprites.append(card.sprite)

        # Retrieve all cards pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        if len(cards_pressed) > 0:
            # Retrieve the top card of the cards at the given location
            card = self.game_info.deck[card_sprites.index(cards_pressed[-1])]
            if len(self.cards_clicked) == 0:
                self.cards_clicked.append(card)
            # Display what happened to the terminal for testing purposes
            print("Card Picked: ", card.getSuit(), card.getRank())

    def on_update(self, delta_time):
        if len(self.cards_clicked) > 0:
            if self.time_one < 0:
                self.time_one = time.time()
            else:
                time_two = time.time()
                if time_two - self.time_one > 2:
                    # self.transition.cut_deck_to_play(self.game_info, self.cards_clicked[0])
                    self.picked_card = self.cards_clicked[0]

                    #Update db
                    self.update_db( card = self.picked_card)

                    #Play animation
                    self.cut_deck_animation()

    #TODO Implement Animation
    def cut_deck_animation(self):
        pass

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

    def update_db(self, card):
        if self.game_info.is_multiplayer:
            self.other_player.send_cut(card = card)