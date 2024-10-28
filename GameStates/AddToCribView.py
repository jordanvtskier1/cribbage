# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game

# Import required files and modules
import arcade
from GameStates import GameInfo
# NOTE: Transition is currently commented out to prevent errors until it is implemented
# from GameStates import StateTransitionBackend
from GameStates.PickCardView import PickCardView

# AddToCribView inherits from PickCardView so that it can use all its methods
# NOTE: As I am writing this Jason presented in class that long lines of inheritence are not 
# good. So I will alter this soon.
class AddToCribView(PickCardView):
    
    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__(game_info)

        # Create variable to keep track of cards selected
        self.cards_clicked = []


    def on_draw(self):
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_deck()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()
        self.draw_crib_button()


    def on_mouse_press(self, x, y, button, modifiers):
        card_sprites = arcade.SpriteList()
        for card in self.game_info.our_hand:
            card_sprites.append(card.sprite)
        # Retrieve all cards pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a card was pressed
        if len(cards_pressed) > 0:
            # Adjust the game state so that the card pressed is moved to the center of play
            card = self.game_info.our_hand[card_sprites.index(cards_pressed[-1])]
            if card not in self.cards_clicked:
                if len(self.cards_clicked) <= 1:
                    self.cards_clicked.append(card)
                    print("Card Picked: ", card.getSuit(), card.getRank())
                else:
                    print("Maximum Number of Cards Already Selected")
            else:
                self.cards_clicked.remove(card)
                print("Card Unpicked: ", card.getSuit(), card.getRank())
        if 35 <= y <= 85 and 175 <= x <= 325:
            if len(self.cards_clicked) >= 2:
                print("Cards Added To Crib: ")
                for card in self.cards_clicked:
                    print(" ", card.getSuit(), card.getRank())
                #crib_view = self.transition.pick_card_to_crib(self.game_info, card)
                #self.window.show_view(crib_view)
            else: 
                print("Not enough Cards picked")

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
            card.setSprite(self.TEST_SPRITE)
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
            card.setSprite(self.TEST_SPRITE)
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
            arcade.draw_rectangle_filled(self.CRIB_LOCATION2[0] + 30, self.CRIB_LOCATION2[1], 150, 125, arcade.color.GRAY)
            arcade.draw_text("Crib", self.CRIB_LOCATION2[0], self.CRIB_LOCATION2[1] + 75, arcade.color.BLACK, 20)
            
            # Draw each card in the crib
            # NOTE: Currently face up need to implement face down
            for card in self.game_info.crib:
                card.setSprite(self.TEST_SPRITE)
                card.setPosition([self.CRIB_LOCATION2[0], self.CRIB_LOCATION2[1]])
                card.draw()

        # Otherwise draw on opps side
        else:
            # Draw an additonal rectangle background and text label for crib
            arcade.draw_rectangle_filled(self.CRIB_LOCATION1[0] + 30, self.CRIB_LOCATION1[1], 150, 125, arcade.color.GRAY)
            arcade.draw_text("Crib", self.CRIB_LOCATION1[0] - 25, self.CRIB_LOCATION1[1] + 75, arcade.color.BLACK, 20)
            # Draw each card in the crib
            for card in self.game_info.crib:
                card.setSprite(self.TEST_SPRITE)
                card.setPosition([self.CRIB_LOCATION1[0], self.CRIB_LOCATION1[1]])
                card.draw()

    def draw_crib_button(self):
        # Draws the deal button
        arcade.draw_rectangle_filled(250, 60, 150, 25, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Add Cards To Crib", 190, 55, arcade.color.BLACK, 11)
        