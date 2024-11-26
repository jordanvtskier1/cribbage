# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import time
import arcade

from Adversary.Multiplayer import Multiplayer
from GameStates import GameInfo
from GameStates.GameView import GameView
from GameStates.StateTransitionBackend import StateTransitionBackend
from Card import Card
from Adversary.CPU import CPU
from Adversary.Multiplayer import Multiplayer



#card.setPosition([self.SCREEN_WIDTH // 4, 175 if self.game_info.is_turn else self.SCREEN_HEIGHT - 175])

class PickCardView(GameView):
    """Class representing the picking card portion of the game"""
    ANIMATION_DURATION = 120

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.tip_string = "Choose a card to see who goes first"
        self.card_picked = None
        self.card_dict = {}
        self.other_card = None
        self.listener = None

        self.OUR_CARD_END_POSITION = [self.SCREEN_WIDTH // 2, 175]
        self.OTHER_CARD_END_POSITION = [self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 175]

        self.set_spread_deck()


    def on_show(self):
        
        self.other_player.pick_card(view = self)
        #if self.game_info.is_multiplayer:
            #Multiplayer.listen_pick_card(view = self)
        #else:
            #Our CPU will act as a mock listener:
            #CPU.pick_card(view = self)

        self.set_spread_deck()


    def is_showing_again(self):
        self.tip_string = "Both players picked the same card!! Pick again :0"


    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """

        self.clear()

        self.draw_spread_deck()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_tips()
        self.animate_cards()

        if self.can_transition():
            self.make_transition()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks.
        Clicking a card to see who goes first.
        """

        # Get card object sprites
        card_sprites = arcade.SpriteList()
        for card in self.game_info.deck:
            card_sprites.append(card.sprite)

        # Retrieve all sprites pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a sprite was pressed
        if len(cards_pressed) > 0 and self.card_picked is None:
            # Retrieve the top card of the cards at the given location
            card = self.game_info.deck[card_sprites.index(cards_pressed[-1])]

            # Display what happened to the terminal for testing purposes
            print("Card Picked: ", card.getSuit(), card.getRank())
            self.card_picked = card

            #start animation
            self.animate_our_card()

            self.update_db(card= self.card_picked)


    def animate_other_card(self):
        self.other_card.start_shake(duration=self.ANIMATION_DURATION,
                                    end_position=self.OTHER_CARD_END_POSITION)


    def animate_our_card(self):
        self.card_picked.start_shake(duration=self.ANIMATION_DURATION,
                                     end_position=self.OUR_CARD_END_POSITION)


    def animate_cards(self):
        for card in [self.card_picked, self.other_card]:
            if card is None:
                continue
            if card.is_animating:
                card.shake_card()


    def can_transition(self):
        for card in [self.card_picked, self.other_card]:
            if card is None:
                return False
            if card.is_animating:
                return False
        return True

    def make_transition(self):
        self.transition.pick_card_to_deal(game_info=self.game_info,
                                              card=self.card_picked,
                                              opponent_card=self.other_card)

    def on_hide_view(self):
        if self.game_info.is_multiplayer:
            self.other_player.database_ref.child(self.game_info.opponent + "/card_pick").delete()

        self.set_spread_deck()


    def update_db(self, card):
        if self.game_info.is_multiplayer:
            self.other_player.send_pick_card(self.game_info, card)