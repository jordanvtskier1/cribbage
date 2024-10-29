# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game


# Import required files and modules
import arcade
from GameStates import GameInfo
from GameStates.GameView import GameView
# NOTE: Transition is currently commented out to prevent errors until it is implemented
# from GameStates.StateTransitionBackend import StateTransitionBackend

# PickCardView inherits from GameView so that it can use the GameView methods
# NOTE: Now inherits from GameView. Benefits: Gets all of GameViews variables and methods
class PickCardView(GameView):

    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__(game_info)


    def on_draw(self):
        """
        The on_draw method draws the components of the game
        """
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_deck()
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

