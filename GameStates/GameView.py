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
        TENTH = 1/10
        HALF = 1/2
        FOURTH = 1/4
        THIRD = 1/3
        EIGHTH = 1/8
        TWENTIETH = 1/20
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 650
        self.DECK_LOCATION = [self.SCREEN_WIDTH * TWENTIETH, self.SCREEN_HEIGHT * HALF]
        self.CRIB_LOCATION1 = [self.SCREEN_WIDTH * TWENTIETH, (self.SCREEN_HEIGHT - self.SCREEN_HEIGHT * FOURTH) + self.SCREEN_HEIGHT * TENTH]
        self.CRIB_LOCATION2 = [self.SCREEN_WIDTH * TWENTIETH, (self.SCREEN_HEIGHT * FOURTH) - self.SCREEN_HEIGHT * TENTH]
        self.YOUR_HAND_LOCATION = [(self.SCREEN_WIDTH * THIRD) + self.SCREEN_WIDTH * TWENTIETH, self.SCREEN_HEIGHT * TENTH]
        self.OPP_HAND_LOCATION = [(self.SCREEN_WIDTH * THIRD) + self.SCREEN_WIDTH * TWENTIETH, self.SCREEN_HEIGHT - self.SCREEN_HEIGHT * TENTH]
        self.CENTER_CARD_LOCATION = [(self.SCREEN_WIDTH * FOURTH) + self.SCREEN_WIDTH * TWENTIETH, self.SCREEN_HEIGHT * HALF]
        self.BOARD_LOCATION = [self.SCREEN_WIDTH - (self.SCREEN_WIDTH * EIGHTH), self.SCREEN_HEIGHT * HALF]
        self.SCORE_LOCATION = [self.SCREEN_WIDTH - (self.SCREEN_WIDTH * EIGHTH), self.SCREEN_HEIGHT * TWENTIETH]
        self.GUIDE_LOCATION = [(self.SCREEN_WIDTH * HALF), self.SCREEN_WIDTH * EIGHTH]
        self.IN_PLAY_LOCATION = [335, 340]
        self.IN_PLAY_X_OFFSET = 40
        self.IN_PLAY_Y_OFFSET = 15

        self.manager = arcade.gui.UIManager()
        self.manager.enable()





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
        TEXT_ADJUSTER_X = 30
        TEXT_ADJUSTER_Y = 75
        RECTANGLE_WIDTH = 75
        RECTANGLE_HEIGHT = 125
        TEXT_SIZE = 20
        arcade.draw_text("Deck", self.DECK_LOCATION[0] - TEXT_ADJUSTER_X, self.DECK_LOCATION[1] + TEXT_ADJUSTER_Y, arcade.color.BLACK, TEXT_SIZE)
        arcade.draw_rectangle_filled(self.DECK_LOCATION[0], self.DECK_LOCATION[1], RECTANGLE_WIDTH, RECTANGLE_HEIGHT, arcade.color.BROWN)
        
        for card in self.game_info.deck:
            #card.setSprite("./Sprites/Cards/card-back.png")
            card.setPosition(self.DECK_LOCATION)
            card.draw()
    

    def draw_scoreboard(self):
        """
        The draw_scoreboard method draws the cribbage board for the game.
        """
        
        # Cribbage board outline
        OUTER_RECTANGLE_WIDTH = 180
        OUTER_RECTANGLE_HEIGHT = 500
        arcade.draw_rectangle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1], OUTER_RECTANGLE_WIDTH, OUTER_RECTANGLE_HEIGHT, arcade.color.BLACK)
        
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
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 205, 5, arcade.color.TAN)
        elif self.game_info.our_score <= 35:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.our_score, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 70, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.our_score, 5, arcade.color.TAN)
        elif self.game_info.our_score <= 38:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 72 + 12 * (self.game_info.our_score - 36), self.BOARD_LOCATION[1] + 155 + 17.5 * (self.game_info.our_score - 36), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 72 + 12 * (self.game_info.our_score - 36), self.BOARD_LOCATION[1] + 155 + 17.5 * (self.game_info.our_score - 36), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 40:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 48 + 18 * (self.game_info.our_score - 38), self.BOARD_LOCATION[1] + 190 + 10 * (self.game_info.our_score - 38), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 48 + 18 * (self.game_info.our_score - 38), self.BOARD_LOCATION[1] + 190 + 10 * (self.game_info.our_score - 38), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 43:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 18 * (self.game_info.our_score - 41), self.BOARD_LOCATION[1] + 210 - 10 * (self.game_info.our_score - 41), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 18 * (self.game_info.our_score - 41), self.BOARD_LOCATION[1] + 210 - 10 * (self.game_info.our_score - 41), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 45:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 48 + 12 * (self.game_info.our_score - 43), self.BOARD_LOCATION[1] + 190 - 17.5 * (self.game_info.our_score - 43), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 48 + 12 * (self.game_info.our_score - 43), self.BOARD_LOCATION[1] + 190 - 17.5 * (self.game_info.our_score - 43), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 80:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 69, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.our_score - 45), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 69, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.our_score - 45), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 83:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 70 - 22 * (self.game_info.our_score - 81), self.BOARD_LOCATION[1] - 205 - 16 * (self.game_info.our_score - 81), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 70 - 22 * (self.game_info.our_score - 81), self.BOARD_LOCATION[1] - 205 - 16 * (self.game_info.our_score - 81), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 85:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 26 - 22 * (self.game_info.our_score - 83), self.BOARD_LOCATION[1] - 237 + 16 * (self.game_info.our_score - 83), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 26 - 22 * (self.game_info.our_score - 83), self.BOARD_LOCATION[1] - 237 + 16 * (self.game_info.our_score - 83), 5, arcade.color.TAN)
        elif self.game_info.our_score <= 120:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 16, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.our_score - 85), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 16, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.our_score - 85), 5, arcade.color.TAN)
        elif self.game_info.our_score >= 121:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 5, arcade.color.TAN)
        
        if self.game_info.other_score == 0:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 205, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 205, 5, arcade.color.TAN)
        elif self.game_info.other_score <= 35:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.other_score, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40, self.BOARD_LOCATION[1] - 193 + 9.37 * self.game_info.other_score, 5, arcade.color.TAN)
        elif self.game_info.other_score <= 40:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40 + 7.5 * (self.game_info.other_score - 36), self.BOARD_LOCATION[1] + 152.5 + 7.5 * (self.game_info.other_score - 36), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] - 40 + 7.5 * (self.game_info.other_score - 36), self.BOARD_LOCATION[1] + 152.5 + 7.5 * (self.game_info.other_score - 36), 5, arcade.color.TAN)
        elif self.game_info.other_score <= 45:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 7.5 * (self.game_info.other_score - 41), self.BOARD_LOCATION[1] + 182.5 - 7.5 * (self.game_info.other_score - 41), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 10 + 7.5 * (self.game_info.other_score - 41), self.BOARD_LOCATION[1] + 182.5 - 7.5 * (self.game_info.other_score - 41), 5, arcade.color.TAN)
        elif self.game_info.other_score <= 80:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 39, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.other_score - 45), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 39, self.BOARD_LOCATION[1] + 146 - 9.42 * (self.game_info.other_score - 45), 5, arcade.color.TAN)
        elif self.game_info.other_score <= 83:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 37.5 - 5 * (self.game_info.other_score - 81), self.BOARD_LOCATION[1] - 192.5 - 5 * (self.game_info.other_score - 81), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 37.5 - 5 * (self.game_info.other_score - 81), self.BOARD_LOCATION[1] - 192.5 - 5 * (self.game_info.other_score - 81), 5, arcade.color.TAN)
        elif self.game_info.other_score <= 85:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 27.5 - 5 * (self.game_info.other_score - 83), self.BOARD_LOCATION[1] - 202.5 + 5 * (self.game_info.other_score - 83), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 27.5 - 5 * (self.game_info.other_score - 83), self.BOARD_LOCATION[1] - 202.5 + 5 * (self.game_info.other_score - 83), 5, arcade.color.TAN)
        elif self.game_info.other_score <= 120:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 14, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.other_score - 85), 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0] + 14, self.BOARD_LOCATION[1] - 194 + 9.42 * (self.game_info.other_score - 85), 5, arcade.color.TAN)
        elif self.game_info.other_score >= 121:
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 6, arcade.color.BLACK)
            arcade.draw_circle_filled(self.BOARD_LOCATION[0], self.BOARD_LOCATION[1] + 155, 5, arcade.color.TAN)


    def draw_score(self):
        """
        The draw_score method draws the score of each player in the game.
        """

        # Draw score box
        OUTER_RECTANGLE_WIDTH = 206
        OUTER_RECTANGLE_HEIGHT = 66
        INNER_RECTANGLE_WIDTH = 200
        INNER_RECTANGLE_HEIGHT = 60
        LINE_ADJUSTER_ONE = 100
        LINE_ADJUSTER_TWO = 50
        LINE_ADJUSTER_THREE = 30
        LINE_WIDTH = 3
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], OUTER_RECTANGLE_WIDTH, OUTER_RECTANGLE_HEIGHT, arcade.color.BLACK)
        arcade.draw_rectangle_filled(self.SCORE_LOCATION[0], self.SCORE_LOCATION[1], INNER_RECTANGLE_WIDTH, INNER_RECTANGLE_HEIGHT, arcade.color.WHITE)
        arcade.draw_line(self.SCORE_LOCATION[0] - LINE_ADJUSTER_ONE, self.SCORE_LOCATION[1], self.SCORE_LOCATION[0] + LINE_ADJUSTER_ONE, self.SCORE_LOCATION[1], arcade.color.BLACK, LINE_WIDTH)
        arcade.draw_line(self.SCORE_LOCATION[0] - LINE_ADJUSTER_TWO, self.SCORE_LOCATION[1] + LINE_ADJUSTER_THREE, self.SCORE_LOCATION[0] - LINE_ADJUSTER_TWO, self.SCORE_LOCATION[1] - LINE_ADJUSTER_THREE, arcade.color.BLACK, LINE_WIDTH)
        arcade.draw_line(self.SCORE_LOCATION[0] + LINE_ADJUSTER_TWO, self.SCORE_LOCATION[1] + LINE_ADJUSTER_THREE, self.SCORE_LOCATION[0] + LINE_ADJUSTER_TWO, self.SCORE_LOCATION[1] - LINE_ADJUSTER_THREE, arcade.color.BLACK, LINE_WIDTH)
        
        # Draw circles to signify player and their color
        CIRCLE_ADJUSTER_X = 75
        CIRCLE_ADJUSTER_Y = 15
        OUTER_CIRCLE_RADIUS = 10
        INNER_CIRCLE_RADIUS = 9
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - CIRCLE_ADJUSTER_X, self.SCORE_LOCATION[1] + CIRCLE_ADJUSTER_Y, OUTER_CIRCLE_RADIUS, arcade.color.BLACK)
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - CIRCLE_ADJUSTER_X, self.SCORE_LOCATION[1] + CIRCLE_ADJUSTER_Y, INNER_CIRCLE_RADIUS, arcade.color.RED)
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - CIRCLE_ADJUSTER_X, self.SCORE_LOCATION[1] - CIRCLE_ADJUSTER_Y, OUTER_CIRCLE_RADIUS, arcade.color.BLACK)
        arcade.draw_circle_filled(self.SCORE_LOCATION[0] - CIRCLE_ADJUSTER_X, self.SCORE_LOCATION[1] - CIRCLE_ADJUSTER_Y, INNER_CIRCLE_RADIUS, arcade.color.BLUE)
        
        TEXT_ADJUSTER_ONE_X = 47
        TEXT_ADJUSTER_TWO_X = 57
        TEXT_ADJUSTER_ONE_Y = 7
        TEXT_ADJUSTER_TWO_Y = 23
        TEXT_SIZE = 15
        # Draw player names
        arcade.draw_text(self.game_info.player, self.SCORE_LOCATION[0] - TEXT_ADJUSTER_ONE_X, self.SCORE_LOCATION[1] + TEXT_ADJUSTER_ONE_Y, arcade.color.BLACK, TEXT_SIZE)
        arcade.draw_text(self.game_info.opponent, self.SCORE_LOCATION[0] - TEXT_ADJUSTER_ONE_X, self.SCORE_LOCATION[1] - TEXT_ADJUSTER_TWO_Y, arcade.color.BLACK, TEXT_SIZE)
        
        # Draw player points
        arcade.draw_text(self.game_info.our_score, self.SCORE_LOCATION[0] + TEXT_ADJUSTER_TWO_X, self.SCORE_LOCATION[1] + TEXT_ADJUSTER_ONE_Y, arcade.color.BLACK, TEXT_SIZE)
        arcade.draw_text(self.game_info.other_score, self.SCORE_LOCATION[0] + TEXT_ADJUSTER_TWO_X, self.SCORE_LOCATION[1] - TEXT_ADJUSTER_TWO_Y, arcade.color.BLACK, TEXT_SIZE)


    def set_our_hand(self):
        CARD_SPACER_INCREMENT = 50
        card_spacer = 0

        for card in self.game_info.our_hand:
            card.setSprite(CardSpriteResolver.getSpriteFile(card.getSuit(), card.getRank()))
            # Adjust cards position if it is clicked
            card.setPosition([self.YOUR_HAND_LOCATION[0] + card_spacer,
                              self.YOUR_HAND_LOCATION[1] ])
            card_spacer += CARD_SPACER_INCREMENT


    def draw_our_hand(self):
        """
        The draw_your_hand method draws the cards in your hand.
        """
        CARD_SPACER_INCREMENT = 50
        CLICKED_ADJUSTER_INCREMENT = 25
        card_spacer = 0

        for card in self.game_info.our_hand:
            if card.is_animating:
                # Adjust cards position if it is clicked
                pos = card.getPosition()
                if card in self.cards_clicked:
                    clicked_adjuster = CLICKED_ADJUSTER_INCREMENT
                    card.setPosition([pos[0],
                                    pos[1]])
                else:
                    card.setPosition([pos[0],
                                pos[1]])
            else:
                clicked_adjuster = 0
                # Adjust cards position if it is clicked
                if card in self.cards_clicked:
                    clicked_adjuster = CLICKED_ADJUSTER_INCREMENT

                card.setPosition([self.YOUR_HAND_LOCATION[0] + card_spacer, self.YOUR_HAND_LOCATION[1] + clicked_adjuster])

                card_spacer += CARD_SPACER_INCREMENT
            card.draw()


    def set_other_hand(self):
        CARD_SPACER_INCREMENT = 50
        card_spacer = 0

        for card in self.game_info.other_hand:
            #card.setSprite("./Sprites/Cards/card-back.png")
            card.setPosition([self.OPP_HAND_LOCATION[0] + card_spacer, self.OPP_HAND_LOCATION[1]])
            card_spacer += CARD_SPACER_INCREMENT


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
        CARD_SPACER_INCREMENT = 20
        RECTANGLE_ADJUSTER = 30
        TEXT_ADJUSTER = 75
        RECTANGLE_WIDTH = 150
        RECTANGLE_HEIGHT = 125
        TEXT_SIZE = 20
        card_spacer = 0

        is_dealer = self.game_info.is_dealer

        # Draw crib label and spot at different locations based on who is dealer
        arcade.draw_rectangle_filled((self.CRIB_LOCATION2[0] if is_dealer else self.CRIB_LOCATION1[0]) + RECTANGLE_ADJUSTER, self.CRIB_LOCATION2[1] if is_dealer else self.CRIB_LOCATION1[1], RECTANGLE_WIDTH, RECTANGLE_HEIGHT,
                                        arcade.color.GRAY)
        arcade.draw_text("Crib", self.CRIB_LOCATION2[0] if is_dealer else self.CRIB_LOCATION1[0], (self.CRIB_LOCATION2[1] if is_dealer else self.CRIB_LOCATION1[1]) + TEXT_ADJUSTER, arcade.color.BLACK, TEXT_SIZE)
        
        for card in self.game_info.crib:
            # card.setSprite("./Sprites/Cards/card-back.png")
            card.setPosition([(self.CRIB_LOCATION2[0] if is_dealer else self.CRIB_LOCATION1[0]) + card_spacer, self.CRIB_LOCATION2[1] if is_dealer else self.CRIB_LOCATION1[1]])
            card_spacer += CARD_SPACER_INCREMENT
            card.draw()


    def get_crib_location(self):
        if self.game_info.is_dealer:
            return CRIB_LOCATION2
        return CRIB_LOCATION1

    def set_spread_deck(self):
        CARD_OFFSET = 10
        CENTER_CARD_ADJUSTER = 100
        card_spacer = 0

        for card in self.game_info.deck:
            # card.setSprite("./Sprites/Cards/card-back.png")
            # If a card is clicked change it's position
            card.setPosition([self.CENTER_CARD_LOCATION[0] - CENTER_CARD_ADJUSTER + card_spacer, self.CENTER_CARD_LOCATION[1]])

            card_spacer += CARD_OFFSET

    def draw_spread_deck(self):
        """
        The draw_spread_deck method draws out the cards in the deck in a spread out fashion.
        """
        for card in self.game_info.deck:
            # card.setSprite("./Sprites/Cards/card-back.png")
            # If a card is clicked change it's position
            card.draw()

    def draw_current_count(self):
        RECTANGLE_ADJUSTER_X = 50
        RECTANGLE_ADJUSTER_Y = 20
        TEXT_ADJUSTER_X = 70
        TEXT_ADJUSTER_Y = 7
        CIRCLE_RADIUS = 25
        TEXT_SIZE = 25
        arcade.draw_circle_filled(self.CENTER_CARD_LOCATION[0] - RECTANGLE_ADJUSTER_X, self.CENTER_CARD_LOCATION[1] + RECTANGLE_ADJUSTER_Y, CIRCLE_RADIUS, arcade.color.GRAY)
        arcade.draw_text(self.game_info.current_count, self.CENTER_CARD_LOCATION[0] - TEXT_ADJUSTER_X, self.CENTER_CARD_LOCATION[1] + TEXT_ADJUSTER_Y, arcade.color.BLACK, TEXT_SIZE)

    def set_cards_in_play(self):
        for card in self.game_info.cards_in_play:
            pos = card.getPosition()
            card.setSprite(CardSpriteResolver.getSpriteFile(card.getSuit(), card.getRank()))
            card.setPosition([pos[0], pos[1]])

    def draw_cards_in_play(self):
        for card in self.game_info.cards_in_play:
            if not card.is_animating:
                card.draw()



    # Returns the next position of the card in play.
    def next_in_play_position(self, is_waiting: bool):
        initial_position_x = self.IN_PLAY_LOCATION[0]
        initial_position_y = self.IN_PLAY_LOCATION[1]
        y_offset = self.IN_PLAY_Y_OFFSET
        x_offset = len( self.game_info.cards_in_play) * self.IN_PLAY_X_OFFSET

        if not is_waiting:
            y_offset *= -1
        return [initial_position_x + x_offset, initial_position_y + y_offset]


    def draw_running_count(self, is_waiting: bool ):
        # We should make it cuter
        y_offset = self.IN_PLAY_Y_OFFSET
        if not is_waiting:
            y_offset *= -1

        card_position = self.next_in_play_position(is_waiting = is_waiting)
        rectangle_position = [card_position[0], card_position[1] + 45 + y_offset]
        arcade.draw_rectangle_filled(center_x= rectangle_position[0], center_y= rectangle_position[1], width = 30, height = 30,
                                     color = arcade.color.ALABAMA_CRIMSON)

    def all_cards_played(self):
        return len(self.game_info.our_hand) == 0 and len(self.game_info.our_hand) == 0
    
    def on_hide_view(self):
        self.manager.disable()