# Menu view will not inherit from Game view

# imports
import arcade
import arcade.gui as gui
from GUI.Buttons.GenericButton import GenericButton
from GameStates.MenuViews.MainMenuView import MainMenuView
from GameStates.StateTransitionBackend import StateTransitionBackend


# A parent class to all views with a text box
# Will take in an extra input of a text label to display on top of the button
# Also a function to transition to our next view once submit is hit
class GameKeyInputView(arcade.View):
    def __init__(self, game_info, state_transition: StateTransitionBackend, label, to_next_view):
        from GameStates.MenuViews.PlayMenuView import PlayMenuView
        super().__init__()
        self.state_transition = state_transition
        self.game_info = game_info
        self.to_next_view = to_next_view
        arcade.set_background_color(arcade.color.GOLD)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        # Create a text label
        self.label = arcade.gui.UILabel(
            text=label,
            text_color=arcade.color.DARK_RED,
            width=350,
            height=40,
            font_size=24,
            font_name="Kenney Future")

        # Create a text input field
        self.input_field = gui.UIInputText(
            color=arcade.color.DARK_BLUE_GRAY,
            font_size=24,
            width=200,
            text='')

        # Create a submit button
        submit_behavior = self.update_text
        submit_button = GenericButton(behavior=submit_behavior, text="Submit", width=200)


        # Make a back button
        back_behavior = lambda: self.window.show_view(
            MainMenuView(game_info=self.game_info, state_transition=self.state_transition)
        )
        back_button = GenericButton(behavior=back_behavior, text="Back", width=200)

        self.v_box = gui.UIBoxLayout()
        self.v_box.add(self.label.with_space_around(bottom=20))
        self.v_box.add(self.input_field)
        self.v_box.add(submit_button)
        self.v_box.add(back_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def update_text(self):
        if self.input_field.text:
            self.to_next_view(self.input_field.text)

    # If we don't disable the manager it will still "draw" the buttons (They are invisible as far as I can tell)
    # But there functions still work, so if on a later view we click where a button was it will do it's function call
    # Which is what was happening. But works with this added.
    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


