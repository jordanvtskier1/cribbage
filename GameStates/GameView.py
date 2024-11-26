"""
View for other views to inherit variables and draw methods from.
CS 3050: Software Engineering
Final Project: Cribbage Game
"""

import arcade

from GUI.Window import CRIB_LOCATION2, CRIB_LOCATION1
from GameStates import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend
from GUI.CardSpriteResolver import CardSpriteResolver

class GameView(arcade.View):
    """Class representing the general view of the game"""


    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):

        super().__init__()
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)

        self.tip_string = ""

        # Represents cards clicked by user
        self.cards_clicked = []

        self.game_info = game_info
        self.other_player = game_info.other_player
        self.transition = state_transition
        
        # Constants for positioning
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
        self.IN_PLAY_LOCATION = [335, 340]
        self.IN_PLAY_X_OFFSET = 40
        self.IN_PLAY_Y_OFFSET = 15


    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """

        self.clear()

        self.draw_deck()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_tips()


    def draw_deck(self):
        """
        The draw_deck method draws each card in the deck.
        """

        # Draw deck label and spot
        arcade.draw_text("Deck", self.DECK_LOCATION[0] - 30, self.DECK_LOCATION[1] + 75, arcade.color.BLACK, 20)
        arcade.draw_rectangle_filled(self.DECK_LOCATION[0], self.DECK_LOCATION[1], 75, 125, arcade.color.BROWN)
        
        for card in self.game_info.deck:
            # card.setSprite("./Sprites/Cards/card-back.png")
            card.setPosition(self.DECK_LOCATION)
            card.draw()
    

    def draw_scoreboard(self):
        """
        The draw_scoreboard method draws the cribbage board for the game.
        """
        
        # Cribbage board outline
        arcade.draw_rectangle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1], 180, 500, arcade.color.BLACK)
        
        score_board = arcade.Sprite("./Sprites/cribbage-board.png", 0.5)
        score_board.center_x = self.BOARD_LOCATION[0]
        score_board.center_y = self.BOARD_LOCATION[1]
        score_board.draw()

    
    def draw_pegs(self):
        """
        The draw_pegs method draws the pegs for the cribbage board.
        """
                
        # TODO: Find better implementation method
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


    def draw_score(self):
        """
        The draw_score method draws the score of each player in the game.
        """

        # Draw score box
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], 206, 66, arcade.color.BLACK)
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], 200, 60, arcade.color.WHITE)
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


    def set_our_hand(self):
        card_spacer = 0

        for card in self.game_info.our_hand:

            # Adjust cards position if it is clicked
            card.setPosition([self.YOUR_HAND_LOCATION[0] + card_spacer,
                              self.YOUR_HAND_LOCATION[1] ])
            card_spacer += 50


    def draw_our_hand(self):
        """
        The draw_your_hand method draws the cards in your hand.
        """

        card_spacer = 0

        for card in self.game_info.our_hand:
            clicked_adjuster = 0
            # Adjust cards position if it is clicked
            if card in self.cards_clicked:
                clicked_adjuster = 25
                pos = card.getPosition()
                card.setPosition([pos[0],
                                  self.YOUR_HAND_LOCATION[1] + clicked_adjuster])

            card.draw()


    def set_other_hand(self):
        card_spacer = 0

        for card in self.game_info.other_hand:
            # card.setSprite("./Sprites/Cards/card-back.png")
            card.setPosition([self.OPP_HAND_LOCATION[0] + card_spacer, self.OPP_HAND_LOCATION[1]])
            card_spacer += 50


    def draw_other_hand(self):
        """
        The draw_opps_hand method draws the cards in your opps hand.
        """
        for card in self.game_info.other_hand:
            card.draw()


    def draw_crib(self):
        """
        The draw_cribbage method draws the cribbage for the game.
        """

        card_spacer = 0

        is_dealer = self.game_info.is_dealer

        # Draw crib label and spot at different locations based on who is dealer
        arcade.draw_rectangle_filled((self.CRIB_LOCATION2[0] if is_dealer else self.CRIB_LOCATION1[0]) + 30, self.CRIB_LOCATION2[1] if is_dealer else self.CRIB_LOCATION1[1], 150, 125,
                                        arcade.color.GRAY)
        arcade.draw_text("Crib", self.CRIB_LOCATION2[0] if is_dealer else self.CRIB_LOCATION1[0], (self.CRIB_LOCATION2[1] if is_dealer else self.CRIB_LOCATION1[1]) + 75, arcade.color.BLACK, 20)
        
        for card in self.game_info.crib:
            # card.setSprite("./Sprites/Cards/card-back.png")
            card.setPosition([(self.CRIB_LOCATION2[0] if is_dealer else self.CRIB_LOCATION1[0]) + card_spacer, self.CRIB_LOCATION2[1] if is_dealer else self.CRIB_LOCATION1[1]])
            card_spacer += 20
            card.draw()


    def get_crib_location(self):
        if self.game_info.is_dealer:
            return CRIB_LOCATION2
        return CRIB_LOCATION1

    def set_spread_deck(self):
        CARD_OFFSET = 10

        card_spacer = 0

        for card in self.game_info.deck:
            # card.setSprite("./Sprites/Cards/card-back.png")
            # If a card is clicked change it's position
            card.setPosition([self.CENTER_CARD_LOCATION[0] - 100 + card_spacer, self.CENTER_CARD_LOCATION[1]])

            card_spacer += CARD_OFFSET

    def draw_spread_deck(self):
        """
        The draw_spread_deck method draws out the cards in the deck in a spread out fashion.
        """
        for card in self.game_info.deck:
            # card.setSprite("./Sprites/Cards/card-back.png")
            # If a card is clicked change it's position
            card.draw()

    def draw_tips(self):
        """
        The draw_tips method draws the tips for the player to help them understand the game
        """
        arcade.draw_rectangle_filled(self.YOUR_HAND_LOCATION[0] + 150, self.YOUR_HAND_LOCATION[1] + 100, 300, 30, arcade.color.LIGHT_GRAY)
        arcade.draw_text(self.tip_string, self.YOUR_HAND_LOCATION[0] + 5, self.YOUR_HAND_LOCATION[1] + 94, arcade.color.BLACK, 10)

    def draw_cards_in_play(self):
        for card in self.game_info.cards_in_play:
            if not card.is_animating:
                card.draw()



    # Returns the next position of the card in play.
    def next_in_play_position(self, opponent: bool):
        initial_position_x = self.IN_PLAY_LOCATION[0]
        initial_position_y = self.IN_PLAY_LOCATION[1]
        y_offset = self.IN_PLAY_Y_OFFSET
        x_offset = len( self.game_info.cards_in_play) * self.IN_PLAY_X_OFFSET

        if not opponent:
            y_offset *= -1
        return [initial_position_x + x_offset, initial_position_y + y_offset]


    def all_cards_played(self):
        return len(self.game_info.cards_in_play) == self.game_info.MAX_PLAYABLE_CARDS - 1



