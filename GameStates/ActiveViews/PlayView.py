import arcade

from Adversary.Multiplayer import Multiplayer
from GameStates.GameInfo import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
from GUI.CardSpriteResolver import CardSpriteResolver
import arcade.gui
from GameStates.StateTransitionBackend import StateTransitionBackend

IN_PLAY_LOCATION = [335, 340]
IN_PLAY_X_OFFSET = 40
IN_PLAY_Y_OFFSET = 15

SCREEN_WIDTH = 1000
CALCULATE_SCORE_POSITION = [(SCREEN_WIDTH // 3), 60]

class PlayView(GameView):

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.has_played = False
        self.picked_card = None
        self.tip_string = "Click on the card you want to play"

        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        # Make a calculate_score_button button
        calculate_score_behavior = lambda : self.transition.play_to_show_score(game_info=game_info)
        quit_button = GenericButton(behavior=calculate_score_behavior,
                                    text="Calculate Score",
                                    width=200)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child = quit_button,
                align_x = CALCULATE_SCORE_POSITION[0],
                align_y = CALCULATE_SCORE_POSITION[1])
        )


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
        self.draw_tips()

        self.play_animation()

        if self.can_transition():
            if self.all_cards_played():
                self.manager.draw()
            else:
                self.make_transition()

    # We assume it is always our turn
    def on_mouse_press(self, x, y, button, modifiers):
        clickable_sprites = arcade.SpriteList()
        for card in self.game_info.our_hand:
            clickable_sprites.append(card.sprite)
        cards_pressed = arcade.get_sprites_at_point((x, y), clickable_sprites)
        if len(cards_pressed) > 0:

            index = clickable_sprites.index(cards_pressed[-1])
            card = self.game_info.our_hand[index]

            #Check if we can click this card, if not we give up on it

            # Play card animation
            if card is not None:
                self.play_card(card)

            # Write to database (we might want to write none?)
            self.update_db(card)


    def update_db(self, card):
        if self.game_info.is_multiplayer:
            Multiplayer.send_play(game_info= self.game_info, card = card)


    def play_animation(self):
        if self.picked_card is not None and self.picked_card.is_animating:
            end_position = self.next_in_play_position(opponent=False)
            self.picked_card.get_dealt_animation(end_position=end_position)


    def play_card(self, card):
        self.has_played = True
        self.picked_card = card
        self.picked_card.is_animating = True


    def can_transition(self):
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
        self.manager.disable()