import arcade

from GUI.PlayerHandDrawer import PlayerHandDrawer
from Game import Game
from Card import Card

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Super Cool Cribbage"
# Positions to begin drawing certain parts of the game
DECK_LOCATION = [50, SCREEN_HEIGHT / 2]
CRIB_LOCATION1 = [50, SCREEN_HEIGHT - SCREEN_HEIGHT / 4]
CRIB_LOCATION2 = [50, SCREEN_HEIGHT / 4]
YOUR_HAND_LOCATION = [SCREEN_WIDTH / 2, 50]
OPP_HAND_LOCATION = [SCREEN_WIDTH / 2,SCREEN_HEIGHT - 50]
CENTER_CARD_LOCATION = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]

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
        # game_state.start_game() Call some method to start game at beggining state
        #self.player_hand = PlayerHandDrawer()
        # <======================================================================>



    def on_mouse_press(self, x, y, button, modifiers):
        """The on_mouse_press inherits from arcade.Window I believe. When the mouse is pressed
        it will call a back end method based both upon what it pressed and the current step within the game/turn
        
        """
        # NOTE: Is currently setup only for the part of a turn where a player plays a 
        # card from their hand into the center.

        # Create a temporary sprite list that matches a player's hand
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
        # Go through each card in the game state deck
        for card in self.game_state.deck:

            # Set Sprites for all cards based on their suit and rank
            card.setSprite("./Sprites/playingCards.png")
            # NOTE: We can use the f strings to get specific card images
            # card.setSource(f"./Sprites/Cards/{card.suit}Suits/{card.rank}_{card.suit}.png")
            
            # Set the position of the cards in the deck to the location the deck should be at in the window
            card.setPosition(DECK_LOCATION)
            
            # Then draw the cards
            card.draw()
    

    def draw_center_cards(self):

        # Spacer to space out the 8 cards that go in the middle during play
        spacer = 0

        # For each card in the cards in play list of game state
        for card in self.game_state.cards_in_play:
            card.setSprite("./Sprites/playingCards.png")
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([CENTER_CARD_LOCATION[0] + spacer, CENTER_CARD_LOCATION[1]])
            spacer += 50
            card.draw()

    def draw_your_hand(self):
        # Spacer to space out the 8 cards that go in the middle during play
        spacer = 0

        # For each card in the cards in play list of game state
        for card in self.game_state.player1_hand:
            card.setSprite("./Sprites/playingCards.png")
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([YOUR_HAND_LOCATION[0] + spacer,YOUR_HAND_LOCATION[1]])
            spacer += 50
            card.draw()

    def draw_opps_hand(self):
        # Spacer to space out the 8 cards that go in the middle during play
        spacer = 0

        # For each card in the cards in play list of game state
        for card in self.game_state.player2_hand:
            card.setSprite("./Sprites/playingCards.png")
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([OPP_HAND_LOCATION[0] + spacer, OPP_HAND_LOCATION[1]])
            spacer += 50
            card.draw()

    def draw_cribbage(self):
        pass

    def draw_score(self):
        pass
            
    def setup(self):
        pass

    def on_draw(self):
        self.clear()


        self.draw_deck()
        self.draw_center_cards()
        self.draw_your_hand()
        self.draw_opps_hand()
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