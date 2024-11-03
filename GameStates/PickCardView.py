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

    global begin_backend_call, wait_for_second_draw
    begin_backend_call = False
    wait_for_second_draw = False

    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__(game_info)


    def on_draw(self):
        """
        The on_draw method draws the components of the game
        """
        global begin_backend_call
        global wait_for_second_draw

        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_spread_deck()
        self.draw_pegs()

        # We still want to draw the card that was picked before the back end is called.
        # So I have moved the call to the backend here so that the drawing may happen first and then
        # after a short delay the backend is called and the view switches.
        # if begin_backend_call:
        #     # We require a second check for if this is the second time on_draw has been called since the
        #     # call to the backend. This is because the on_draw method does not fully draw until it completes.
        #     # So we have to wait for the second call of on_draw.
        #     # Will ask Professor Hibbeler during class
        #     if wait_for_second_draw:
        #         # This is causing a crash
        #         # time.sleep(0.5)
        #
        #         # Back end transition call TESTING
        #         # self.transition.pick_card_to_add_crib(self.game_info, self.cards_clicked[0])
        #     else:
        #         wait_for_second_draw = True


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

            # Display what happened to the terminal for testing purposes
            print("Card Picked: ", card.getSuit(), card.getRank())
            self.transition.pick_card_to_add_crib(game_info= self.game_info, card = card)
            # A variable to denote when to begin calling the back end in on_draw
            # global begin_backend_call
            # begin_backend_call = True




    def draw_spread_deck(self):
        """
        The draw_spread_deck method draws out the cards in the deck in a spread out fashion
        """
        # Offset to space cards, so that they overlap eachother like a fanned out deck
        card_offset = 0
        # For each card in the deck
        for card in self.game_info.deck:
            # Draw it to match a fanned out deck on the screen
            if card in self.cards_clicked:
                if self.game_info.is_turn:
                    card.setPosition([self.SCREEN_WIDTH // 2, 100])
                else:
                    card.setPosition([self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 100])
            else:
                card.setPosition([self.CENTER_CARD_LOCATION[0] - 100 + card_offset, self.CENTER_CARD_LOCATION[1]])
            card.draw()
            card_offset += 10

