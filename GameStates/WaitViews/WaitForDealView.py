# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade

from GUI.Window import TRUE_CENTER
from GameStates import GameInfo
from GameStates.GameView import GameView
import arcade.gui
from GameStates.StateTransitionBackend import StateTransitionBackend
from Card import Card

WAITING_STRING = "Waiting . . ."
SHUFFLING_STRING = "Shuffling . . ."
DEALING_STRING = "You are the Dealer!"

MESSAGE_BOX_POSITION = [-175, -250]


class WaitForDealView(GameView):
    """Class representing the adding cards to the crib portion of the game"""
    WAITING_DECK_POSITION = TRUE_CENTER

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.listener_done = False

        # Setup add to crib button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        message = self.resolve_tip_string()
        self.message_box = arcade.gui.UILabel(
            text=message,
            text_color=arcade.color.DARK_RED,
            width=500,
            height=40,
            font_size=24,
            font_name="Kenney Future")

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=self.message_box,
                align_x=MESSAGE_BOX_POSITION[0],
                align_y=MESSAGE_BOX_POSITION[1])
        )

        self.waiting_deck = Card(position=self.WAITING_DECK_POSITION)
        self.min_wait = 120

    def on_show(self):
        if not self.game_info.is_dealer:
            self.other_player.listen_to_deal(view=self)

    def resolve_tip_string(self):
        if self.game_info.is_dealer:
            return SHUFFLING_STRING
        else:
            return WAITING_STRING

    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """
        self.clear()
        self.manager.draw()

        if not self.done_dealing():
            self.waiting_animation()
        else:
            self.dealing_animation()
            if self.can_transition():
                self.transition.wait_deal_to_add_crib(game_info=self.game_info)

    def on_hide_view(self):
        self.manager.disable()

    def waiting_animation(self):
        self.waiting_deck.spin_once()
        self.waiting_deck.draw()

    def done_dealing(self):
        if self.game_info.is_dealer:
            # Pretend to be dealing for some time
            if self.min_wait <= 0:
                return True
            self.min_wait -= 1
            if self.min_wait == 0:
                self.change_dealing_message()
            return False
        else:
            return self.listener_done

    def change_dealing_message(self):
        # self.manager.remove(self.message_box)
        self.message_box.text = DEALING_STRING
        # self.manager.add(self.message_box)

    def dealing_animation(self):

        # If it is done spinning
        if self.waiting_deck.stop_spinning_animation():
            card_spacer = 0
            for card in self.game_info.our_hand:
                end_position = [self.YOUR_HAND_LOCATION[0] + card_spacer, self.YOUR_HAND_LOCATION[1]]
                card.get_dealt_animation(end_position=end_position)
                card_spacer += 50

            card_spacer = 0
            for card in self.game_info.other_hand:
                end_position = [self.OPP_HAND_LOCATION[0] + card_spacer, self.OPP_HAND_LOCATION[1]]
                card.get_dealt_animation(end_position=end_position)
                card_spacer += 50

    def can_transition(self):
        for card in self.game_info.our_hand:
            if card.is_animating:
                return False
        for card in self.game_info.other_hand:
            if card.is_animating:
                return False
        return True