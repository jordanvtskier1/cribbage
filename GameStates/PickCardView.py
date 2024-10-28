# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import arcade
from GameStates import GameInfo
#from GameStates.StateTransitionBackend import StateTransitionBackend


class PickCardView(arcade.View):

    def __init__(self, game_info: GameInfo):
        super().__init__()
        self.game_info = game_info
        #self.transition = self.StateTransitionBackend()
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)

        # Set Locations to draw components of the game
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
        self.TEST_SPRITE = "./Sprites/PlayingCards.png"




    def on_draw(self):
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_spread_deck()


    def on_mouse_press(self, x, y, button, modifiers):
        card_sprites = arcade.SpriteList()
        for card in self.game_info.deck:
            card_sprites.append(card.sprite)
        # Retrieve all cards pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a card was pressed
        if len(cards_pressed) > 0:
            # Adjust the game state so that the card pressed is moved to the center of play
            card = self.game_info.deck[card_sprites.index(cards_pressed[-1])]
            #crib_view = self.transition.pick_card_to_crib(self.game_info, card)
            #self.window.show_view(crib_view)
            print("Card Picked: ", card.getSuit(), card.getRank())
    
    def draw_scoreboard(self):
        """
        The draw_scoreboard method draws the cribbage board for the game. It does this by using a sprite for the
        board in the SPRITES folder and placing it on the right middle of the scren.
        """
        # Add text label to scoreboard
        arcade.draw_text("Scoreboard", self.BOARD_LOCATION[0] - 90, self.BOARD_LOCATION[1] + 260, arcade.color.BLACK, 25)
        # Image I found online for 3 person/NOTE: Change to two person later
        score_board = arcade.Sprite("./Sprites/cribbage-board.png", 0.5)
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
        arcade.draw_text("Player 1", self.SCORE_LOCATION[0] - 38, self.SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text("Player 2", self.SCORE_LOCATION[0] - 38, self.SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)
        # Draw player points
        arcade.draw_text(self.game_info.our_score, self.SCORE_LOCATION[0] + 57, self.SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text(self.game_info.other_score, self.SCORE_LOCATION[0] + 57, self.SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)


    def draw_spread_deck(self):

        card_offset = 0

        for card in self.game_info.deck:
            card.setPosition([self.CENTER_CARD_LOCATION[0] - 100 + card_offset, self.CENTER_CARD_LOCATION[1]])
            card.draw()
            card_offset += 10


