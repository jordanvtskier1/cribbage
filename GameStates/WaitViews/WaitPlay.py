import arcade

from GameStates.GameInfo import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
from GUI.CardSpriteResolver import CardSpriteResolver
import arcade.gui
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU
from GameStates.StateTransitionBackend import StateTransitionBackend


CALCULATE_SCORE_Y = -200
CALCULATE_SCORE_X = -50
SCREEN_WIDTH = 1000
CALCULATE_SCORE_POSITION = [(SCREEN_WIDTH // 3), 60]

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
                align_x = -50,
                align_y = -250)
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

        self.play_animation()

        if self.can_transition():
            if self.all_cards_played():
                self.manager.draw()
            else:
                self.make_transition()




    def on_hide_view(self):
        self.manager.disable()


    # We need to either show a message that a card could not be played or put the card in the center
    def play_animation(self):
        if self.picked_card is not None and self.picked_card.is_animating:
            end_position = self.next_in_play_position(opponent=True)
            self.picked_card.get_dealt_animation(end_position= end_position)


    def card_was_played(self, card):
        self.listener_done = True
        self.picked_card = card
        self.picked_card.is_animating = True


    # TODO add logic for when other player cant play
    def can_transition(self):
        if (self.listener_done
                and
                self.picked_card is not None
                and not
                self.picked_card.is_animating):
            return True
        return False

    def make_transition(self):
        self.transition.wait_to_play(game_info = self.game_info, card = self.picked_card)


