# Menu view will not inherit from Game view

# imports
import arcade
import arcade.gui as gui
from GUI.Buttons.GenericButton import GenericButton
from GameStates.MenuViews.MainMenuView import MainMenuView
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.GameInfo import GameInfo


# A parent class to all views with a text box
# Will take in an extra input of a text label to display on top of the button
# Also a function to transition to our next view once submit is hit
class EndGameView(arcade.View):
    def __init__(self, game_info, state_transition: StateTransitionBackend):
        from GameStates.MenuViews.PlayMenuView import PlayMenuView
        super().__init__()
        self.state_transition = state_transition
        self.game_info = game_info
        arcade.set_background_color(arcade.color.GOLD)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()
        label = ""
        if self.game_info.our_win == True:
            label = f"Congrats {self.game_info.player} you won!"
        else:
            label = f"Better luck next time..."


        # Create a text label
        end_label = arcade.gui.UILabel(
            text=label,
            text_color=arcade.color.DARK_RED,
            width=550,
            height=40,
            font_size=24,
            font_name="Kenney Future")

        # Create a submit button
        menu_behavior = lambda: self.window.show_view(MainMenuView(game_info=GameInfo(), state_transition=StateTransitionBackend(self.window)))
        menu_button = GenericButton(behavior=menu_behavior, text="Menu", width=200)

        self.v_box = gui.UIBoxLayout()
        self.v_box.add(end_label.with_space_around(bottom=20))
        self.v_box.add(menu_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )


    # If we don't disable the manager it will still "draw" the buttons (They are invisible as far as I can tell)
    # But there functions still work, so if on a later view we click where a button was it will do it's function call
    # Which is what was happening. But works with this added.
    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


