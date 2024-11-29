import arcade

from Adversary.Multiplayer import Multiplayer
from Backend.BackendFunctions import Backend
from GameStates.GameInfo import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
from GUI.CardSpriteResolver import CardSpriteResolver
from Card import Card
import arcade.gui
from GameStates.StateTransitionBackend import StateTransitionBackend
from Backend.BackendFunctions import Backend

IN_PLAY_LOCATION = [335, 340]
IN_PLAY_X_OFFSET = 40
IN_PLAY_Y_OFFSET = 15

BUTTON_ALIGN = [-50, -250]
SCREEN_WIDTH = 1000


class PlayView(GameView):

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.has_played = False
        self.picked_card = None
        self.tip_string = "Click on the card you want to play"

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


        self.manager2 = arcade.gui.UIManager()
        # Make a calculate_score_button button
        calculate_score_behavior = lambda : self.transition.play_to_show_score(game_info=game_info)
        quit_button = GenericButton(behavior=calculate_score_behavior,
                                    text="Calculate Score",
                                    width=200)

        self.manager2.add(
            arcade.gui.UIAnchorWidget(
                child = quit_button,
                align_x = BUTTON_ALIGN[0],
                align_y = BUTTON_ALIGN[1])
        )

        self.we_can_play = self.check_can_we_play()

    def on_show(self):
        self.set_cards_in_play()

        if not self.we_can_play:
            self.we_cant_play()


    def on_draw(self):
        self.clear()
        self.draw_deck()
        self.draw_crib()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_cards_in_play()
        self.draw_current_count()

        self.play_animation()
        self.manager.draw()

        if self.can_transition():
            if self.all_cards_played() or not self.we_can_play:
                self.manager2.enable()
                self.manager2.draw()
            else:
                self.make_transition()

    # We assume it is always our turn
    def on_mouse_press(self, x, y, button, modifiers):
        if self.picked_card is None and self.we_can_play:
            clickable_sprites = arcade.SpriteList()
            for card in self.game_info.our_hand:
                clickable_sprites.append(card.sprite)
            cards_pressed = arcade.get_sprites_at_point((x, y), clickable_sprites)
            if len(cards_pressed) > 0:

                index = clickable_sprites.index(cards_pressed[-1])
                card = self.game_info.our_hand[index]

                #Check if we can click this card, if not we give up on it

                # Play card animation
                if card is not None and Backend.can_play_card(self.game_info, card):
                    self.play_card(card)

                    # Write to database (we might want to write none?)
                    self.update_db(card)
                elif not Backend.can_play_card(self.game_info, card):
                    self.tip_message = "You can't play this card as it would make the board value exceed 31."


    def update_db(self, card):
        if self.game_info.is_multiplayer:
            Multiplayer.send_play(game_info= self.game_info, card = card)


    def play_animation(self):
        if self.picked_card is not None and self.picked_card.is_animating:
            end_position = self.next_in_play_position(is_waiting =False)
            self.picked_card.get_dealt_animation(end_position=end_position)


    def play_card(self, card):

        self.has_played = True
        self.picked_card = card
        self.picked_card.is_animating = True


    def can_transition(self):
        if not self.we_can_play:
            return True

        if (self.has_played
            and
            self.picked_card is not None
            and
            self.picked_card.is_animating is False):

                return True
        return False


    def make_transition(self):
        self.transition.play_to_wait(game_info=self.game_info, card= self.picked_card)


    def on_hide_view(self):
        self.manager2.disable()

    def check_can_we_play(self):
        return Backend.can_we_play(self.game_info)

    def we_cant_play(self):

        empty_card = Card.create_empty_card()

        self.update_db(card = empty_card)
        self.picked_card = empty_card

        self.tip_string = "You cant play any cards!"
        self.tip_message.message_text = self.tip_string

        self.make_cant_play_button()


    def make_cant_play_button(self):
        self.manager2.clear()

        behavior = lambda: self.make_transition()
        button = GenericButton(behavior=behavior,
                                    text="Pass turn",
                                    width=200)
        self.manager2.add(
            arcade.gui.UIAnchorWidget(
                child = button,
                align_x = BUTTON_ALIGN[0],
                align_y = BUTTON_ALIGN[1] - 30)
        )