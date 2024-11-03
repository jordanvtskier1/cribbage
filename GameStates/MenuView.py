# Menu view will not inherit from Game view

# imports
import arcade
import arcade.gui
from GUI.Buttons.GenericButton import GenericButton
from GameStates.StateTransitionBackend import StateTransitionBackend


class MenuView(arcade.View):
    def __init__(self, game_info, state_transition: StateTransitionBackend):
        super().__init__()
        self.state_transition = state_transition
        self.game_info = game_info
        arcade.set_background_color(arcade.color.GOLD)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        # Make a start button
        start_behavior = lambda : self.state_transition.menu_to_pick_card(self.game_info)

        start_button = GenericButton(behavior = start_behavior, text = 'Start', width= 200)
        self.v_box.add(start_button.with_space_around(bottom = 20))

        # Make a quit button
        quit_behavior = lambda : arcade.exit()
        quit_button = GenericButton(behavior=quit_behavior, text= "Quit", width=200)
        self.v_box.add(quit_button)


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


