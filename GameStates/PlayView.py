import arcade

from GameStates.GameInfo import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
import arcade.gui

from GameStates.StateTransitionBackend import StateTransitionBackend

IN_PLAY_LOCATION = [335, 340]
IN_PLAY_X_OFFSET = 40
IN_PLAY_Y_OFFSET = 15
#Make 8 once we are done with other player
MAX_PLAYABLE_CARDS = 8


CALCULATE_SCORE_Y = -200
CALCULATE_SCORE_X = -75

class PlayView(GameView):

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        # Make a calculate_score_button button
        calculate_score_behavior = lambda : self.transition.play_to_show_score(game_info=game_info)
        quit_button = GenericButton(behavior=calculate_score_behavior,
                                    text="Calculate Score",
                                    width=200)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=quit_button,
                align_y = CALCULATE_SCORE_Y,
                align_x = CALCULATE_SCORE_X)
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
        if len(self.game_info.cards_in_play) == MAX_PLAYABLE_CARDS:
            self.manager.draw()

    # We assume it is always our turn
    def on_mouse_press(self, x, y, button, modifiers):
        clickable_sprites = arcade.SpriteList()
        for card in self.game_info.our_hand:
            clickable_sprites.append(card.sprite)
        cards_pressed = arcade.get_sprites_at_point((x, y), clickable_sprites)
        if len(cards_pressed) > 0:

            index = clickable_sprites.index(cards_pressed[-1])
            card = self.game_info.our_hand[index]
            self.transition.play_to_wait(game_info = self.game_info, card = card)

    def draw_cards_in_play(self):
        initialPositionX = IN_PLAY_LOCATION[0]
        initialPositionY = IN_PLAY_LOCATION[1]
        y_offset = IN_PLAY_Y_OFFSET
        x_offset = 0
        # We have no way of knowing who played what so cards are placed in an alternating up and down manner
        if self.game_info.is_dealer:
             y_offset *= -1
        for card in self.game_info.cards_in_play:
            card.setPosition([initialPositionX + x_offset, initialPositionY + y_offset])
            card.draw()
            x_offset += IN_PLAY_X_OFFSET
            y_offset *= -1

    def on_hide_view(self):
        self.manager.disable()