import arcade
import GameInfo

class GameState:

    representableSprites = arcade.SpriteList()
    clickableSprites = arcade.SpriteList()
    gameInfo = GameInfo.GameInfo()

    def __init__(self, game_info: GameInfo):
       self.gameInfo = game_info

    def on_draw(self):
        pass
    def on_click(self):
        pass
