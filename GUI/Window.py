import arcade

from GUI.PlayerHandDrawer import PlayerHandDrawer
from Game import Game
from Card import Card

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"
TEST_SPRITE = "./Sprites/Cards/WormSuits/K_Worm.png"
# Positions to begin drawing certain parts of the game
# Kind of wonky rn subject to change/adjustment
DECK_LOCATION = [50, SCREEN_HEIGHT / 2]
CRIB_LOCATION1 = [50, (SCREEN_HEIGHT - SCREEN_HEIGHT / 4) + 50]
CRIB_LOCATION2 = [50, (SCREEN_HEIGHT / 4) - 50]
YOUR_HAND_LOCATION = [(SCREEN_WIDTH // 3), 60]
OPP_HAND_LOCATION = [(SCREEN_WIDTH // 3), SCREEN_HEIGHT - 68]
CENTER_CARD_LOCATION = [(SCREEN_WIDTH // 4) + 50, SCREEN_HEIGHT / 2]
BOARD_LOCATION = [SCREEN_WIDTH - (SCREEN_WIDTH // 8), SCREEN_HEIGHT / 2]
SCORE_LOCATION = [SCREEN_WIDTH - (SCREEN_WIDTH // 8), SCREEN_HEIGHT // 18]

class Window(arcade.Window):
    def __init__(self):

        # Initialize Window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GUPPIE_GREEN)
        
        # Create game state object
        self.game_state = Game()

        # <====================== FOR TESTING FUNCTIONS =========================>
        self.game_state.create_deck(self.game_state.SUITS, self.game_state.CARD_VALUES)
        self.game_state.deal_hands(self.game_state.DEAL)
        self.game_state.crib.append(Card("",""))
        # game_state.start_game() Call some method to start game at beggining state
        #self.player_hand = PlayerHandDrawer()
        # <======================================================================>



    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press inherits from arcade.Window I believe. When the mouse is pressed
        it will call a back end method based both upon what it pressed and the current step within the game/turn
        """
        # NOTE: Is currently setup only for the part of a turn where a player plays a 
        # card from their hand into the center. Currently no other actions coded.

        # Create a temporary sprite list that matches a player's hand
        if (self.game_state.player1_turn == True and self.game_state.is_player1 == True) or (self.game_state.player1_turn == False and self.game_state.is_player1 == False):
            card_sprites = arcade.SpriteList()
            for card in self.game_state.player1_hand:
                card_sprites.append(card.sprite)
            # Retrieve all cards pressed at the given location
            cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

            # As long as a card was pressed
            if len(cards_pressed) > 0:
                # Adjust the game state so that the card pressed is moved to the center of play
                self.game_state.card_played(card_sprites.index(cards_pressed[-1]))


    def draw_deck(self):
        """
        The draw_deck method draws each card in the deck. It does this by retrieving the deck variable in
        game_state and drawing each card to the middle left of the screen.
        """
        # Draw a rectangle under the deck to help signify it's location
        arcade.draw_text("Deck", DECK_LOCATION[0] - 30, DECK_LOCATION[1] + 75, arcade.color.BLACK, 20)
        arcade.draw_rectangle_filled(DECK_LOCATION[0], DECK_LOCATION[1], 75, 125, arcade.color.BROWN)
        
        # Go through each card in the deck
        for card in self.game_state.deck:
            # Set Sprites for all cards based on their suit and rank
            # NOTE: Currently just using base image
            card.setSprite("./Sprites/playingCards.png")
            # NOTE: We can use the f strings to get specific card images
            # card.setSource(f"./Sprites/Cards/{card.suit}Suits/{card.rank}_{card.suit}.png")
            
            # Set the position of the cards in the deck to the location the deck should be at in the window
            card.setPosition(DECK_LOCATION)
            
            # Then draw each card
            card.draw()
    

    def draw_center_cards(self):
        """
        The draw_center_cards method draws the cards that are currently in play. It does this by retrieving
        each card in the game_state cards_in_play variable and drawing them in the center of the screen.
        """
        # A spacer so that cards are not drawn directly on top of one another
        card_spacer = 0
        # To offset every other card in height slightly
        offset = False

        # For each card in play
        for card in self.game_state.cards_in_play:
            # Set the card sprite/card img
            card.setSprite(TEST_SPRITE)
            # Adjust by the spacer so cards are not on top of eachother
            # Make every other card slightly higher just like in cribbage online example
            # Draw in Center card location
            if offset:
                card.setPosition([CENTER_CARD_LOCATION[0] + card_spacer, CENTER_CARD_LOCATION[1] + 25])
            else:
                card.setPosition([CENTER_CARD_LOCATION[0] + card_spacer, CENTER_CARD_LOCATION[1]])
            card_spacer += 50
            offset = not offset
            card.draw()


    def draw_your_hand(self):
        """
        The draw_your_hand method draws the cards in your hand. It does this by retrieving the correct 
        hand list for you from the game_state and displaying it on the bottom middle of the screen.
        """
        # Spacer to space out the cards in hand
        card_spacer = 0

        # Determine which player you are
        your_hand = self.game_state.player1_hand
        if self.game_state.is_player1 == True:
            your_hand = self.game_state.player1_hand
        else:
            your_hand = self.game_state.player2_hand

        # For each card in hand
        for card in your_hand:
            card.setSprite(TEST_SPRITE)
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([YOUR_HAND_LOCATION[0] + card_spacer, YOUR_HAND_LOCATION[1]])
            card_spacer += 50
            card.draw()


    def draw_opps_hand(self):
        """
        The draw_opps_hand method draws the cards in your opps hand. It does this by retrieving the correct 
        hand list for your opp from the game_state and displaying it on the top middle of the screen.
        """
        # Spacer to space out the cards in hand
        card_spacer = 0

        # Determine which player your opp is    
        opps_hand = self.game_state.player2_hand
        if self.game_state.is_player1 == True:
            opps_hand = self.game_state.player2_hand
        else:
            opps_hand = self.game_state.player1_hand

        # For each card in hand
        for card in opps_hand:
            card.setSprite(TEST_SPRITE)
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([OPP_HAND_LOCATION[0] + card_spacer, OPP_HAND_LOCATION[1]])
            card_spacer += 50
            card.draw()


    def draw_cribbage(self):
        """
        The draw_cribbage method draws the cribbage on the side of whose turn it is. It does this by retrieving
        the proper game_state information to determine which player you are and if it is that players turn, it
        the correctly draws the cribbage on that side.
        """
        # If it is your turn draw the crib on your side
        if (self.game_state.player1_turn == True and self.game_state.is_player1 == True) or (self.game_state.player1_turn == False and self.game_state.is_player1 == False):
            # Draw an additonal rectangle background and text label for crib
            arcade.draw_rectangle_filled(CRIB_LOCATION2[0] + 30, CRIB_LOCATION2[1], 150, 125, arcade.color.GRAY)
            arcade.draw_text("Crib", CRIB_LOCATION2[0], CRIB_LOCATION2[1] + 75, arcade.color.BLACK, 20)
            
            # Draw each card in the crib
            # NOTE: Currently face up need to implement face down
            for card in self.game_state.crib:
                card.setSprite(TEST_SPRITE)
                card.setPosition([CRIB_LOCATION2[0], CRIB_LOCATION2[1]])
                card.draw()

        # Otherwise draw on opps side
        else:
            # Draw an additonal rectangle background and text label for crib
            arcade.draw_rectangle_filled(CRIB_LOCATION1[0] + 30, CRIB_LOCATION1[1], 150, 125, arcade.color.GRAY)
            arcade.draw_text("Crib", CRIB_LOCATION1[0] - 25, CRIB_LOCATION1[1] + 75, arcade.color.BLACK, 20)
            # Draw each card in the crib
            for card in self.game_state.crib:
                card.setSprite(TEST_SPRITE)
                card.setPosition([CRIB_LOCATION1[0], CRIB_LOCATION1[1]])
                card.draw()
        

    def draw_scoreboard(self):
        """
        The draw_scoreboard method draws the cribbage board for the game. It does this by using a sprite for the
        board in the SPRITES folder and placing it on the right middle of the scren.
        """
        # Add text label to scoreboard
        arcade.draw_text("Scoreboard", BOARD_LOCATION[0] - 90, BOARD_LOCATION[1] + 260, arcade.color.BLACK, 25)
        # Image I found online for 3 person/NOTE: Change to two person later
        score_board = arcade.Sprite("./Sprites/cribbage-board.png", 0.5)
        score_board.center_x = BOARD_LOCATION[0]
        score_board.center_y = BOARD_LOCATION[1]
        score_board.draw()


    def draw_score(self):
        """
        The draw_score method draws the score of each player in the game. It does this by using a rectangle to create
        a background and text to draw out each players information.
        """
        # Draw background white rectangle
        arcade.draw_rectangle_filled(SCORE_LOCATION[0], SCORE_LOCATION[1], 200, 60, arcade.color.WHITE)
        # Draw lines to make boxes in rectangle
        arcade.draw_line(SCORE_LOCATION[0] - 100, SCORE_LOCATION[1], SCORE_LOCATION[0] + 100, SCORE_LOCATION[1], arcade.color.BLACK, 3)
        arcade.draw_line(SCORE_LOCATION[0] - 50, SCORE_LOCATION[1] + 30, SCORE_LOCATION[0] - 50, SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        arcade.draw_line(SCORE_LOCATION[0] + 50, SCORE_LOCATION[1] + 30, SCORE_LOCATION[0] + 50, SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        # Draw border of rectangle
        arcade.draw_line(SCORE_LOCATION[0] - 101, SCORE_LOCATION[1] + 30, SCORE_LOCATION[0] + 101, SCORE_LOCATION[1] + 30, arcade.color.BLACK, 3)
        arcade.draw_line(SCORE_LOCATION[0] - 101, SCORE_LOCATION[1] - 30, SCORE_LOCATION[0] + 101, SCORE_LOCATION[1] - 30, arcade.color.BLACK, 3)
        arcade.draw_line(SCORE_LOCATION[0] + 100, SCORE_LOCATION[1] - 31, SCORE_LOCATION[0] + 100, SCORE_LOCATION[1] + 31, arcade.color.BLACK, 3)
        arcade.draw_line(SCORE_LOCATION[0] - 100, SCORE_LOCATION[1] - 31, SCORE_LOCATION[0] - 100, SCORE_LOCATION[1] + 31, arcade.color.BLACK, 3)
        # Draw squares to signify player and their color
        arcade.draw_rectangle_filled(SCORE_LOCATION[0] - 75, SCORE_LOCATION[1] + 15, 10, 10, arcade.color.RED)
        arcade.draw_rectangle_filled(SCORE_LOCATION[0] - 75, SCORE_LOCATION[1] - 15, 10, 10, arcade.color.BLUE)
        # Draw player names
        arcade.draw_text("Player 1", SCORE_LOCATION[0] - 38, SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text("Player 2", SCORE_LOCATION[0] - 38, SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)
        # Draw player points
        arcade.draw_text(self.game_state.player1_score, SCORE_LOCATION[0] + 57, SCORE_LOCATION[1] + 7, arcade.color.BLACK, 15)
        arcade.draw_text(self.game_state.player2_score, SCORE_LOCATION[0] + 57, SCORE_LOCATION[1] - 23, arcade.color.BLACK, 15)
            

    def setup(self):
        pass


    def on_draw(self):
        # Clear window
        self.clear()

        # Call methods to draw certain components of the game
        self.draw_deck()
        self.draw_center_cards()
        self.draw_your_hand()
        self.draw_opps_hand()
        self.draw_cribbage()
        self.draw_scoreboard()
        self.draw_score()

        # Test
        #self.player_hand.addSprite(300, 300)
        """
        
        self.center_cards.draw()
        self.other_player_cards.draw()
        self.cribbage.draw()
        self.score.draw()
        
        """
        #self.player_hand.draw()

        """
        Wait for user input ( clicking on cards or hovering )
        #Call back end
        windowUpdate = BackEnd.execute(userInput, GameState)
        
        # use window update on front endn
        """
