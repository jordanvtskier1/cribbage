# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game


# Import required files and modules
import arcade
from GameStates import GameInfo
# NOTE: Transition is currently commented out to prevent errors until it is implemented
# from GameStates.StateTransitionBackend import StateTransitionBackend

# GameView inherits from arcade.View so that it can use the built in py arcade methods
# NOTE: Now each of our views inherits from this one view. Benefits: Less duplicated code and
# all children also get the LOCATIONS constants and some draw methods.

# NOTE: Still working on inheritance because there is still duplicated code. Should discuss on Wednesday

class GameView(arcade.View):

    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__()

        self.cards_clicked = []

        # Create game_info and transition objects
        self.game_info = game_info
        # self.transition = self.StateTransitionBackend()
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)

        # Constants to represent locations on the screen for drawing components of the game.
        # These are set as class variables so that the views that come after this view can inherit them
        # To reduce duplicated code, so all children of GameView have these variables
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 650  
        self.DECK_LOCATION = [50, self.SCREEN_HEIGHT / 2]
        self.CRIB_LOCATION1 = [50, (self.SCREEN_HEIGHT - self.SCREEN_HEIGHT / 4) + 50]
        self.CRIB_LOCATION2 = [50, (self.SCREEN_HEIGHT / 4) - 50]
        self.YOUR_HAND_LOCATION = [(self.SCREEN_WIDTH // 3) + 50, 60]
        self.OPP_HAND_LOCATION = [(self.SCREEN_WIDTH // 3) + 50, self.SCREEN_HEIGHT - 68]
        self.CENTER_CARD_LOCATION = [(self.SCREEN_WIDTH // 4) + 50, self.SCREEN_HEIGHT / 2]
        self.BOARD_LOCATION = [self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 8), self.SCREEN_HEIGHT / 2]
        self.SCORE_LOCATION = [self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 8), self.SCREEN_HEIGHT // 18]

        # NOTE: Currently for testing until card sprites are finished
        self.TEST_SPRITE = "./Sprites/Cards/WormSuits/K_Worm.png"


    def on_draw(self):
        """
        The on_draw method draws the components of the game
        """
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_deck()
    

    def draw_scoreboard(self):
        """
        The draw_scoreboard method draws the cribbage board for the game. It does this by using a sprite for the
        board in the SPRITES folder and placing it on the right middle of the screen.
        """
        # Add text label to scoreboard
        arcade.draw_text("Scoreboard", self.BOARD_LOCATION[0] - 90, self.BOARD_LOCATION[1] + 260, arcade.color.BLACK, 25)
        # NOTE: I am using a sprite image found online which may not be what we want, but it works for testing
        score_board = arcade.Sprite("./Sprites/cribbage-board.png", 0.5)
        
        # Set the sprites location to the BOARD_LOCATION
        score_board.center_x = self.BOARD_LOCATION[0]
        score_board.center_y = self.BOARD_LOCATION[1]
        score_board.draw()


    def draw_score(self):
        """
        The draw_score method draws the score of each player in the game. It does this by using a rectangle to create
        a background and text to draw out each players information.
        """
        # Draw background white rectangle
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], 200, 60, arcade.color.WHITE)
        # Draw lines to make boxes in rectangle
        arcade.draw_line(self.SCORE_LOCATION[0] - 100, self.SCORE_LOCATION[1], self.SCORE_LOCATION[0] + 100, self.SCORE_LOCATION[1], arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] - 50, self.SCORE_LOCATION[1] + 30, self.SCORE_LOCATION[0] - 50, self.SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] + 50, self.SCORE_LOCATION[1] + 30, self.SCORE_LOCATION[0] + 50, self.SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        # Draw border of rectangle
        arcade.draw_line(self.SCORE_LOCATION[0] - 101, self.SCORE_LOCATION[1] + 30, self.SCORE_LOCATION[0] + 101, self.SCORE_LOCATION[1] + 30, arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] - 101, self.SCORE_LOCATION[1] - 30, self.SCORE_LOCATION[0] + 101, self.SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] + 100, self.SCORE_LOCATION[1] - 31, self.SCORE_LOCATION[0] + 100, self.SCORE_LOCATION[1] + 31, arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] - 100, self.SCORE_LOCATION[1] - 31, self.SCORE_LOCATION[0] - 100, self.SCORE_LOCATION[1] + 31, arcade.color.BLACK, 3)
        # Draw squares to signify player and their color
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0] - 75, self.SCORE_LOCATION[1] + 15, 10, 10, arcade.color.RED)
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0] - 75, self.SCORE_LOCATION[1] - 15, 10, 10, arcade.color.BLUE)
        # Draw player names
        arcade.draw_text("You", self.SCORE_LOCATION[0] - 38, self.SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text("Computer", self.SCORE_LOCATION[0] - 38, self.SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)
        # Draw player points
        arcade.draw_text(self.game_info.our_score, self.SCORE_LOCATION[0] + 57, self.SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text(self.game_info.other_score, self.SCORE_LOCATION[0] + 57, self.SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)


    def draw_deck(self):
        """
        The draw_deck method draws each card in the deck. It does this by retrieving the deck variable in
        game_state and drawing each card to the middle left of the screen.
        """
        # Draw a rectangle under the deck to help signify it's location
        arcade.draw_text("Deck", self.DECK_LOCATION[0] - 30, self.DECK_LOCATION[1] + 75, arcade.color.BLACK, 20)
        arcade.draw_rectangle_filled(self.DECK_LOCATION[0], self.DECK_LOCATION[1], 75, 125, arcade.color.BROWN)
        
        # Go through each card in the deck
        for card in self.game_info.deck:
            # Set Sprites for all cards based on their suit and rank
            # NOTE: Currently just using base image
            card.setSprite("./Sprites/playingCards.png")
            # NOTE: We can use the f strings to get specific card images
            # card.setSource(f"./Sprites/Cards/{card.suit}Suits/{card.rank}_{card.suit}.png")
            
            # Set the position of the cards in the deck to the location the deck should be at in the window
            card.setPosition(self.DECK_LOCATION)
            
            # Then draw each card
            card.draw() 

