import arcade
from GameStates.oldStates.GameState import GameState
from GameInfo import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend


class DealState(GameState):
    representableSprites = arcade.SpriteList()
    clickableSprites = arcade.SpriteList()

    def __init__(self, game_info: GameInfo):
        super().__init__(game_info)

    def on_draw(self):
        # draw deck
        # draw scoreboard
        # draw DEAL button
        pass

    def on_click(self) -> GameState:
        # Check for click on DEAL button
        # Call backend to implement deal logic (shuffle deck)
        if button.clicked:
            # If we deal we change states

            return StateTransitionBackend.deal_to_add_to_crib(game_state= self)
        else:
            # If we dont deal we stay in this state
            return self
