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

