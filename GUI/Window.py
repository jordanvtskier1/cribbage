import arcade

from GUI.PlayerHandDrawer import PlayerHandDrawer

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"

class Window(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)
        self.player_hand = PlayerHandDrawer()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()


        # Test
        self.player_hand.addSprite( 180, 65)
        """
        
        self.center_cards.draw()
        self.other_player_cards.draw()
        self.cribbage.draw()
        self.score.draw()
        
        """
        self.player_hand.draw()

        """
        Wait for user input ( clicking on cards or hovering )
        #Call back end
        windowUpdate = BackEnd.execute(userInput, GameState)
        
        # use window update on front endn
        """