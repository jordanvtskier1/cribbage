# View for cutting the deck
# CS 3050: Software Engineering
# Final Project: Cribbage Game

import arcade
from GameStates import GameInfo
# from GameStates import StateTransitionBackend
from GameStates.AddToCribView import AddToCribView


# CutDeckView inherits from AddToCribView so that it can use all its methods
# NOTE: As I am writing this Jason presented in class that long lines of inheritence are not 
# good. So I will alter this soon.
class CutDeckView(AddToCribView):
    
    def __init__(self, game_info: GameInfo):
        super().__init__(game_info)

    def on_draw(self):
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_deck()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()
        self.draw_crib_button()
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