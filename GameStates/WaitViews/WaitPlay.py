import arcade

from GameStates.GameInfo import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
from GUI.CardSpriteResolver import CardSpriteResolver
import arcade.gui
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU

from GameStates.StateTransitionBackend import StateTransitionBackend

IN_PLAY_LOCATION = [335, 340]
IN_PLAY_X_OFFSET = 40
IN_PLAY_Y_OFFSET = 15
#Make 8 once we are done with other player
MAX_PLAYABLE_CARDS = 8


CALCULATE_SCORE_Y = -200
CALCULATE_SCORE_X = -75

class WaitPlayView(GameView):

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Make a calculate_score_button button
        calculate_score_behavior = lambda : self.transition.play_to_show_score(game_info=game_info)
        score_button = GenericButton(behavior=calculate_score_behavior,
                                    text="Calculate Score",
                                    width=200)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=score_button,
                align_y = CALCULATE_SCORE_Y,
                align_x = CALCULATE_SCORE_X)
        )
        
        self.tip_string = "Wait for opponent's play . . ."
        self.listener_done = False
        self.picked_card = None

    def on_show(self):
        self.set_our_hand()
        self.set_other_hand()

        if self.game_info.is_multiplayer:
            pass
        else:
            CPU.listen_to_play(view = self)


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
        if len(self.game_info.cards_in_play) == MAX_PLAYABLE_CARDS:
            self.manager.draw()


    def draw_cards_in_play(self):
        initial_position_x = IN_PLAY_LOCATION[0]
        initial_position_y = IN_PLAY_LOCATION[1]
        y_offset = IN_PLAY_Y_OFFSET
        x_offset = 0
        # We have no way of knowing who played what so cards are placed in an alternating up and down manner
        if self.game_info.is_dealer:
             y_offset *= -1
        for card in self.game_info.cards_in_play:
            card.setPosition([initial_position_x + x_offset, initial_position_y + y_offset])
            card.draw()
            x_offset += IN_PLAY_X_OFFSET
            y_offset *= -1

    def on_hide_view(self):
        self.manager.disable()

    # TODO add logic for when other player cant play
    def can_transition(self):
        if (self.listener_done
            and not
            self.picked_card.is_animating):
            return True
        return False


    # We need to either show a message that a card could not be played or put the card in the center
    def play_animation(self):

        #TODO Need to calculate this!
        end_position = [500, 500]

        if self.picked_card.is_animating:
            self.picked_card.get_dealt_animation(end_position= end_position)

    def card_was_played(self, card):
        self.listener_done = True
        self.picked_card = card
        self.picked_card.is_animating = True