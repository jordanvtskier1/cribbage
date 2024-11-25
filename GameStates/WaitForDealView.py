# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade

from Backend_test import game_info
from GUI.Window import TRUE_CENTER
from GameStates import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
import arcade.gui
from GameStates.StateTransitionBackend import StateTransitionBackend
from Card import Card
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU



class WaitForDealView(GameView):
    """Class representing the adding cards to the crib portion of the game"""
    WAITING_DECK_POSITION = TRUE_CENTER

    
    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)


        self.listener_done = False
        self.tip_string = "Choose a two cards to add to the crib"

        # Setup add to crib button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        waiting_box = arcade.gui.UILabel(
            text="Waiting . . .",
            text_color=arcade.color.DARK_RED,
            width=350,
            height=40,
            font_size=24,
            font_name="Kenney Future")
 

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=waiting_box,
                align_x = -250,
                align_y = -250)
        )
        
        self.waiting_deck = Card(position= self.WAITING_DECK_POSITION)

    def on_show(self):
        if self.game_info.is_multiplayer:
            Multiplayer.listen_to_deal(view = self)
        else: 
            CPU.listen_to_deal(view = self)


    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """
        self.clear()
        self.manager.draw()
        if not self.listener_done:
            self.waiting_animation()
        if self.listener_done:
            self.dealing_animation()
            if self.can_transition():
                self.transition.wait_deal_to_add_crib(game_info = self.game_info)

        
    def on_hide_view(self):
        self.manager.disable()

    def waiting_animation(self):
        self.waiting_deck.spin_once()
        self.waiting_deck.draw()

    def dealing_animation(self):

        # If it is done spinning
        if self.waiting_deck.stop_spinning_animation():
            card_spacer = 0
            for card in self.game_info.our_hand:
                end_position = [self.YOUR_HAND_LOCATION[0] + card_spacer, self.YOUR_HAND_LOCATION[1]]
                card.get_dealt_animation(end_position = end_position)
                card_spacer += 50

            card_spacer = 0
            for card in self.game_info.other_hand:
                end_position = [self.OPP_HAND_LOCATION[0] + card_spacer, self.OPP_HAND_LOCATION[1]]
                card.get_dealt_animation(end_position = end_position)
                card_spacer += 50

    def can_transition(self):
        for card in self.game_info.our_hand:
            if card.is_animating:
                return False
        for card in self.game_info.other_hand:
            if card.is_animating:
                return False
        return True