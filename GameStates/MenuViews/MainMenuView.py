# Menu view will not inherit from Game view

# imports
import arcade
import arcade.gui
from GUI.Buttons.GenericButton import GenericButton
from GameStates.StateTransitionBackend import StateTransitionBackend


class MainMenuView(arcade.View):
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

        game_title = arcade.gui.UILabel(
            text=" BUG CRIBBAGE !!! :O",
            text_color=arcade.color.DARK_RED,
            width=350,
            height=40,
            font_size=24,
            font_name="Kenney Future")
        self.v_box.add(game_title)

        # Make a start button
        play_behavior = lambda : self.window.show_view(
            PlayMenuView(game_info= self.game_info, state_transition= self.state_transition)
        )

        play_button = GenericButton(behavior = play_behavior, text = 'Play', width= 200)
        self.v_box.add(play_button.with_space_around(bottom = 20))

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


