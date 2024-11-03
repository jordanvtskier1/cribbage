import arcade
import arcade.gui
from arcade.gui import UIOnClickEvent


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class GenericButton(arcade.gui.UIFlatButton):
    def __init__(self, behavior, **kwargs):
        super().__init__(**kwargs)
        self.behavior = behavior

    def on_click(self, event: UIOnClickEvent):
        self.behavior()
