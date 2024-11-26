# Menu view will not inherit from Game view

# imports
import arcade
import arcade.gui
from GameStates.GameView import GameView

from GameStates.GameInfo import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend

class ShowScoreView(GameView):
    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition= state_transition)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        message_box_behavior = lambda x : self.transition.show_score_to_crib(self.game_info)
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=(
                "Your score is: " + str(self.game_info.our_score) +
                "\n Player 2 Score is: " + str(self.game_info.other_score)
            ),
            callback= message_box_behavior,
            buttons=["Ok"]
        )

        self.v_box.add(message_box)


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.draw_pegs()
        self.draw_scoreboard()
        self.draw_score()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()


