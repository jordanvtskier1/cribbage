# Menu view will not inherit from Game view

# imports
import arcade
import arcade.gui
from GUI.Buttons.GenericButton import GenericButton
from Adversary.CPU import CPU

from GameStates.StateTransitionBackend import StateTransitionBackend


class PlayMenuView(arcade.View):
    def __init__(self, game_info, state_transition: StateTransitionBackend):
        from GameStates.MenuViews.MainMenuView import MainMenuView

        from GameStates.MenuViews.JoinInputView import JoinInputView

        super().__init__()
        self.state_transition = state_transition
        self.game_info = game_info
        arcade.set_background_color(arcade.color.GOLD)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        # Make a host_game button
        host_button = GenericButton(behavior = self.host_behavior, text = 'Host Game', width= 200)
        self.v_box.add(host_button.with_space_around(bottom = 20))

        join_button = GenericButton(behavior=self.join_behavior, text='Join Game', width=200)
        self.v_box.add(join_button.with_space_around(bottom=20))

        cpu_button = GenericButton(behavior = self.cpu_behavior, text = 'Play vs CPU ( Start game in dev mode)', width= 200)
        self.v_box.add(cpu_button.with_space_around(bottom = 20))

        # Make a back button
        back_behavior = lambda : self.window.show_view(
            MainMenuView(game_info=self.game_info, state_transition=self.state_transition)
        )
        back_button = GenericButton(behavior=back_behavior, text= "Back", width=200)
        self.v_box.add(back_button)


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

    def host_behavior(self):
        from GameStates.MenuViews.HostInputView import HostInputView

        self.game_info.is_multiplayer = True
        self.window.show_view(
            HostInputView(game_info=self.game_info, state_transition=self.state_transition)
        )

    def join_behavior(self):
        from GameStates.MenuViews.JoinInputView import JoinInputView

        self.game_info.is_multiplayer = True
        self.window.show_view(
            JoinInputView(game_info=self.game_info, state_transition=self.state_transition)
        )


    def cpu_behavior(self):
        self.game_info.is_multiplayer = False
        self.state_transition.set_other_player( other_player_logic= CPU() )
        self.state_transition.menu_to_pick_card(game_info=self.game_info)