# View for picking a card to see who goes first
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade
from GameStates import GameInfo
from GameStates.GameView import GameView
from GameStates.StateTransitionBackend import StateTransitionBackend
from Card import Card

class PickCardView(GameView):
    """Class representing the picking card portion of the game"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.tip_string = "Choose a card to see who goes first"
        self.db_ref = state_transition.database_ref
        self.card_picked = None
        self.card_dict = {}
        self.other_card = None
        self.listener = None

    def on_show(self):

        self.listen()

    def listen(self):

        def listener(event):
            print(event.event_type)  # can be 'put' or 'patch'
            print(event.path)  # relative to the reference, it seems
            print(event.data)  # new data at /reference/event.path. None if deleted

            if event.data is not None:
                self.card_dict = event.data
                self.other_card = Card( event.data["suit"], event.data["rank"] )

        self.listener = self.db_ref.child(self.game_info.opponent + "/card_pick").listen(listener)


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

        if self.other_card is not None and self.card_picked is not None:
            self.transition.pick_card_to_add_crib(game_info=self.game_info,
                                                  card=self.card_picked,
                                                  opponent_card = self.other_card)



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
            self.card_picked = card
            query = {
                self.game_info.player: {'card_pick': card.getDict()}
            }
            self.db_ref.update(query)

    def on_hide_view(self):
        self.db_ref.child(self.game_info.opponent + "/card_pick").delete()