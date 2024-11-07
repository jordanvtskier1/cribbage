# View for cutting the deck
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import arcade
from GameStates import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.GameView import GameView


# CutDeckView inherits from GameView so that it can use all its methods
# NOTE: Now inherits from GameView. Benefits: Gets all of GameViews variables and methods
class CutDeckView(GameView):
    
    def __init__(self, game_info: GameInfo):
        super().__init__(game_info)

    def on_draw(self):
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_pegs()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()
        self.draw_spread_deck()
    
    def on_mouse_press(self, x, y, button, modifiers):

        # if self.game_info.is_turn:
        card_sprites = arcade.SpriteList()
        for card in self.game_info.deck:
            card_sprites.append(card.sprite)
        # Retrieve all cards pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a card was pressed
        if len(cards_pressed) > 0:
            # Adjust the game state so that the card pressed is moved to the center of play
            card = self.game_info.deck[card_sprites.index(cards_pressed[-1])]
            print("Card Picked: ", card.getSuit(), card.getRank())
            self.transition.cut_deck_to_play(self.game_info, card)

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
            # Adjust by the spacer so cards are not on top of eachother
            card.setPosition([self.OPP_HAND_LOCATION[0] + card_spacer, self.OPP_HAND_LOCATION[1]])
            card_spacer += 50
            card.draw()
        
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