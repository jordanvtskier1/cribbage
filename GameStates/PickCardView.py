# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade
from GameStates import GameInfo
from GameStates.GameView import GameView
from GameStates.StateTransitionBackend import StateTransitionBackend


class PickCardView(GameView):
    """Class representing the picking card portion of the game"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.tip_string = "Choose a card to see who goes first"


    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """

        self.clear()

        self.draw_spread_deck()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_tips()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks.
        Clicking a card to see who goes first.
        """

        # Get card object sprites
        card_sprites = arcade.SpriteList()
        for card in self.game_info.deck:
            card_sprites.append(card.sprite)

        # Retrieve all sprites pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a sprite was pressed
        if len(cards_pressed) > 0:
            # Retrieve the top card of the cards at the given location
            card = self.game_info.deck[card_sprites.index(cards_pressed[-1])]

            # Display what happened to the terminal for testing purposes
            print("Card Picked: ", card.getSuit(), card.getRank())
            self.transition.pick_card_to_add_crib(game_info= self.game_info, card = card)
