# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game


# Import required files and modules
import arcade
import time
import math
import random
from GameStates import GameInfo
from GameStates.GameView import GameView
from GameStates.AddToCribView import AddToCribView
from GameStates.StateTransitionBackend import StateTransitionBackend

# PickCardView inherits from GameView so that it can use the GameView methods
# NOTE: Now inherits from GameView. Benefits: Gets all of GameViews variables and methods
class PickCardView(GameView):

    # global begin_backend_call, wait_for_second_draw
    # begin_backend_call = False
    # wait_for_second_draw = False

    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__(game_info)


    def on_draw(self):
        """
        The on_draw method draws the components of the game
        """
        # global begin_backend_call
        # global wait_for_second_draw

        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_spread_deck()
        self.draw_pegs()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks
        """
        pass
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

            # Display what happened to the terminal for testing purposes
            print("Card Picked: ", card.getSuit(), card.getRank())
            # Need a way to have program draw card picked for user to see before this call to the transition,
            # so that they know which card they picked. Current method was causing error so discuss monday
            self.transition.pick_card_to_add_crib(game_info= self.game_info, card = card)
            # A variable to denote when to begin calling the back end in on_draw
            # global begin_backend_call
            # begin_backend_call = True