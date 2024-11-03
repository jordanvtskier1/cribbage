import arcade
from GameStates import GameInfo

class GameState(arcade.View):

    representableSprites = arcade.SpriteList()
    clickableSprites = arcade.SpriteList()
    gameInfo = GameInfo.GameInfo()

    def __init__(self, game_info: GameInfo):
       super().__init__()
       self.gameInfo = game_info

    def on_draw(self):
        pass
    def on_click(self):
        pass
