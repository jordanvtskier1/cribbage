import arcade
from GameStates.GameState import GameState
from GameInfo import GameInfo


class AddToCribState(GameState):
    representableSprites = arcade.SpriteList()
    clickableSprites = arcade.SpriteList()

    def __init__(self, game_info: GameInfo):
        super().__init__( game_info)

    def on_draw(self):
        # draw deck
        # draw scoreboard
        # draw crib
        # draw hand
        pass

    def on_click(self):
        # wait for two clicks on cards
        pass