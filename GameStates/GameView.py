"""
View for picking a card to see who goes first
CS 3050: Software Engineering
Final Project: Cribbage Game
"""


# Import required files and modules
import arcade
from GameStates import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend
from GUI.CardSpriteResolver import CardSpriteResolver

# GameView inherits from arcade.View so that it can use the built in py arcade methods
# NOTE: Now each of our views inehrits from this one view. Benefits: Less duplicated code and
# all children also get the LOCATIONS constants and some draw methods.

# NOTE: Still working on inheritance becuase there is still duplicated code.
# Should discuss on Wednesday

class GameView(arcade.View):
    """Class representing the general view of the game"""

    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__()

        self.cards_clicked = []

        # Create game_info and transition objects
        self.game_info = game_info
        self.transition = StateTransitionBackend(self.window)
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)

        # Constants to represent locations on the screen for drawing compoenents of the game.
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


    def on_draw(self):
        """
        The on_draw method draws the components of the game
        """
        self.clear()
        self.draw_scoreboard()
        self.draw_pegs()
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
        arcade.draw_rectangle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1], 180, 500, arcade.color.BLACK)
        # Set the sprites location to the BOARD_LOCATION
        score_board.center_x = self.BOARD_LOCATION[0]
        score_board.center_y = self.BOARD_LOCATION[1]
        score_board.draw()


    def draw_score(self):
        """
        The draw_score method draws the score of each player in the game. It does this by using a rectangle to create
        a background and text to draw out each players information.
        """
        # Draw border of rectangle
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], 206, 66, arcade.color.BLACK)
        # Draw background white rectangle
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], 200, 60, arcade.color.WHITE)
        # Draw lines to make boxes in rectangle
        arcade.draw_line(self.SCORE_LOCATION[0] - 100, self.SCORE_LOCATION[1], self.SCORE_LOCATION[0] + 100, self.SCORE_LOCATION[1], arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] - 50, self.SCORE_LOCATION[1] + 30, self.SCORE_LOCATION[0] - 50, self.SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        arcade.draw_line(self.SCORE_LOCATION[0] + 50, self.SCORE_LOCATION[1] + 30, self.SCORE_LOCATION[0] + 50, self.SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        # Draw circles to signify player and their color
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - 75, self.SCORE_LOCATION[1] + 15, 6, arcade.color.BLACK)
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - 75, self.SCORE_LOCATION[1] + 15, 5, arcade.color.RED)
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - 75, self.SCORE_LOCATION[1] - 15, 6, arcade.color.BLACK)
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - 75, self.SCORE_LOCATION[1] - 15, 5, arcade.color.BLUE)
        # Draw player names
        arcade.draw_text("You", self.SCORE_LOCATION[0] - 47, self.SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text("Computer", self.SCORE_LOCATION[0] - 47, self.SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)
        # Draw player points
        arcade.draw_text(self.game_info.our_score, self.SCORE_LOCATION[0] + 57, self.SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text(self.game_info.other_score, self.SCORE_LOCATION[0] + 57, self.SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)

    def draw_pegs(self):
        """
        Draws the pegs for the game board.
        NOTE: Currently implemented very poorly, if I have time I will try to improve this. But it works. - Carson
        """
        if self.game_info.our_score == 0:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 205, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 205, 5, arcade.color.RED)
        elif self.game_info.our_score <= 35:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.our_score, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.our_score, 5, arcade.color.RED)
        elif self.game_info.our_score <= 38:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 72 + 12 * (self.game_info.our_score - 36), self.BOARD_LOCATION[1] + 155 + 17.5 * (self.game_info.our_score - 36), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 72 + 12 * (self.game_info.our_score - 36), self.BOARD_LOCATION[1] + 155 + 17.5 * (self.game_info.our_score - 36), 5, arcade.color.RED) 
        elif self.game_info.our_score <= 40:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 48 + 18 * (self.game_info.our_score - 38), self.BOARD_LOCATION[1] + 190 + 10 * (self.game_info.our_score - 38), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 48 + 18 * (self.game_info.our_score - 38), self.BOARD_LOCATION[1] + 190 + 10 * (self.game_info.our_score - 38), 5, arcade.color.RED) 
        elif self.game_info.our_score <= 43:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 18 * (self.game_info.our_score - 41), self.BOARD_LOCATION[1] + 210 - 10 * (self.game_info.our_score - 41), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 18 * (self.game_info.our_score - 41), self.BOARD_LOCATION[1] + 210 - 10 * (self.game_info.our_score - 41), 5, arcade.color.RED) 
        elif self.game_info.our_score <= 45:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 48 + 12 * (self.game_info.our_score - 43), self.BOARD_LOCATION[1] + 190 - 17.5 * (self.game_info.our_score - 43), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 48 + 12 * (self.game_info.our_score - 43), self.BOARD_LOCATION[1] + 190 - 17.5 * (self.game_info.our_score - 43), 5, arcade.color.RED) 
        elif self.game_info.our_score <= 80:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 69, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.our_score - 45), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 69, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.our_score - 45), 5, arcade.color.RED)
        elif self.game_info.our_score <= 83:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 70 - 22 * (self.game_info.our_score - 81), self.BOARD_LOCATION[1] - 205 - 16 * (self.game_info.our_score - 81), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 70 - 22 * (self.game_info.our_score - 81), self.BOARD_LOCATION[1] - 205 - 16 * (self.game_info.our_score - 81), 5, arcade.color.RED) 
        elif self.game_info.our_score <= 85:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 26 - 22 * (self.game_info.our_score - 83), self.BOARD_LOCATION[1] - 237 + 16 * (self.game_info.our_score - 83), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 26 - 22 * (self.game_info.our_score - 83), self.BOARD_LOCATION[1] - 237 + 16 * (self.game_info.our_score - 83), 5, arcade.color.RED) 
        elif self.game_info.our_score <= 120:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 16, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.our_score - 85), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 16, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.our_score - 85), 5, arcade.color.RED)
        elif self.game_info.our_score >= 121:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 5, arcade.color.RED)
        
        if self.game_info.other_score == 0:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 205, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 205, 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 35:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.other_score, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.other_score, 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 40:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40 + 7.5 * (self.game_info.other_score - 36), self.BOARD_LOCATION[1] + 152.5 + 7.5 * (self.game_info.other_score - 36), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40 + 7.5 * (self.game_info.other_score - 36), self.BOARD_LOCATION[1] + 152.5 + 7.5 * (self.game_info.other_score - 36), 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 45:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 7.5 * (self.game_info.other_score - 41), self.BOARD_LOCATION[1] + 182.5 - 7.5 * (self.game_info.other_score - 41), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 7.5 * (self.game_info.other_score - 41), self.BOARD_LOCATION[1] + 182.5 - 7.5 * (self.game_info.other_score - 41), 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 80:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 39, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.other_score - 45), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 39, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.other_score - 45), 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 83:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 37.5 - 5 * (self.game_info.other_score - 81), self.BOARD_LOCATION[1] - 192.5 - 5 * (self.game_info.other_score - 81), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 37.5 - 5 * (self.game_info.other_score - 81), self.BOARD_LOCATION[1] - 192.5 - 5 * (self.game_info.other_score - 81), 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 85:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 27.5 - 5 * (self.game_info.other_score - 83), self.BOARD_LOCATION[1] - 202.5 + 5 * (self.game_info.other_score - 83), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 27.5 - 5 * (self.game_info.other_score - 83), self.BOARD_LOCATION[1] - 202.5 + 5 * (self.game_info.other_score - 83), 5, arcade.color.BLUE)
        elif self.game_info.other_score <= 120:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 14, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.other_score - 85), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 14, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.other_score - 85), 5, arcade.color.BLUE)
        elif self.game_info.other_score >= 121:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 5, arcade.color.BLUE)

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

            # Set the position of the cards in the deck to the location the deck should be at in the window
            card.setPosition(self.DECK_LOCATION)
         
            # Then draw each card
            card.draw()

    def draw_our_hand(self):
        """
        The draw_your_hand method draws the cards in your hand. It does this by retrieving the correct 
        hand list for you from the game_state and displaying it on the bottom middle of the screen.
        """
        # Spacer to space out the cards in hand
        card_spacer = 0

        clicked_adjuster = 25

        # For each card in hand
        for card in self.game_info.our_hand:
            # Adjust by the spacer so cards are not on top of eachother
            if card in self.cards_clicked:
                card.setPosition([self.YOUR_HAND_LOCATION[0] + card_spacer, self.YOUR_HAND_LOCATION[1] + clicked_adjuster])
            else:
                card.setPosition([self.YOUR_HAND_LOCATION[0] + card_spacer, self.YOUR_HAND_LOCATION[1]])

            card_spacer += 50
            card.draw()

    def draw_other_hand(self):
        """
        The draw_opps_hand method draws the cards in your opps hand. It does this by retrieving the correct 
        hand list for your opp from the game_state and displaying it on the top middle of the screen.
        """
        # Spacer to space out the cards in hand
        card_spacer = 0

        # For each card in hand
        for card in self.game_info.other_hand:
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([self.OPP_HAND_LOCATION[0] + card_spacer, self.OPP_HAND_LOCATION[1]])
            card_spacer += 50
            card.draw()

    def draw_crib(self):
        """
        The draw_cribbage method draws the cribbage on the side of whose turn it is. It does this by retrieving
        the proper game_state information to determine which player you are and if it is that players turn, it
        the correctly draws the cribbage on that side.
        """
        # If it is your turn draw the crib on your side
        if self.game_info.is_dealer:
            # Draw an additonal rectangle background and text label for crib
            arcade.draw_rectangle_filled(self.CRIB_LOCATION2[0] + 30, self.CRIB_LOCATION2[1], 150, 125,
                                         arcade.color.GRAY)
            arcade.draw_text("Crib", self.CRIB_LOCATION2[0], self.CRIB_LOCATION2[1] + 75, arcade.color.BLACK, 20)
            offset = 0
            # Draw each card in the crib
            # NOTE: Currently face up need to implement face down
            for card in self.game_info.crib:
                card.setPosition([self.CRIB_LOCATION2[0] + offset, self.CRIB_LOCATION2[1]])
                offset += 20
                card.draw()

        # Otherwise draw on opps side
        else:
            # Draw an additonal rectangle background and text label for crib
            arcade.draw_rectangle_filled(self.CRIB_LOCATION1[0] + 30, self.CRIB_LOCATION1[1], 150, 125,
                                         arcade.color.GRAY)
            arcade.draw_text("Crib", self.CRIB_LOCATION1[0] - 25, self.CRIB_LOCATION1[1] + 75, arcade.color.BLACK, 20)
            offset = 0
            # Draw each card in the crib
            for card in self.game_info.crib:
                card.setPosition([self.CRIB_LOCATION1[0] + offset, self.CRIB_LOCATION1[1]])
                offset += 20
                card.draw()
