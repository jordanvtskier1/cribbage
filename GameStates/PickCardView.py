# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game


# Import required files and modules
import arcade
from GameStates import GameInfo
# NOTE: Transition is currently commented out to prevent errors until it is implemented
# from GameStates.StateTransitionBackend import StateTransitionBackend

# PickCardView inherits from arcade.View so that it can use the built in py arcade methods
# NOTE: As I am writing this Jason presented in class that long lines of inheritence are not 
# good. So I will alter this soon.
class PickCardView(arcade.View):

    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__()

        # Create game_info and transition objects
        self.game_info = game_info
        # self.transition = self.StateTransitionBackend()
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)

        # Constants to represent locations on the screen for drawing compoenents of the game.
        # These are set as class variables so that the views that come after this view can inherit them
        # To reduce duplicated code, so all children of PickCardView have these variables
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
        self.TEST_SPRITE = "./Sprites/PlayingCards.png"


    def on_draw(self):
        """
        The on_draw method draws the components of the game
        """
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_spread_deck()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks
        """

        # Create a sprite list to hold card sprites
        card_sprites = arcade.SpriteList()

        # Add the sprites from each card in the deck to the sprite list
        for card in self.game_info.deck:
            card_sprites.append(card.sprite)

        # Retrieve all sprites pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a sprite was pressed at the location
        if len(cards_pressed) > 0:
            # Retrieve the top card of the cards at the given location
            card = self.game_info.deck[card_sprites.index(cards_pressed[-1])]

            # NOTE: Here is where the call to transition would take place.
            # crib_view = self.transition.pick_card_to_crib(self.game_info, card)
            # self.window.show_view(crib_view)

            # Display what happened to the terminal for testing purposes
            print("Card Picked: ", card.getSuit(), card.getRank())
    

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


    def draw_spread_deck(self):
        """
        The draw_spread_deck method draws out the cards in the deck in a spread out fashion
        """
        # Offset to space cards, so that they overlap eachother like a fanned out deck
        card_offset = 0

        # For each card in the deck
        for card in self.game_info.deck:
            # Draw it to match a fanned out deck on the screen
            card.setPosition([self.CENTER_CARD_LOCATION[0] - 100 + card_offset, self.CENTER_CARD_LOCATION[1]])
            card.draw()
            card_offset += 10

