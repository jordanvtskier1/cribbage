# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade

from Backend_test import game_info
from GameStates import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
import arcade.gui
from GameStates.StateTransitionBackend import StateTransitionBackend
from Card import Card
from Adversary.Multiplayer import Multiplayer
from Adversary.CPU import CPU

class AddToCribView(GameView):
    """Class representing the adding cards to the crib portion of the game"""

    def __init__(self, game_info: GameInfo, state_transition: StateTransitionBackend):
        super().__init__(game_info, state_transition)

        self.added_to_crib = False
        self.crib_location = self.get_crib_location()

        self.cards_to_crib = []
        self.tip_string = "Choose a two cards to add to the crib"

        # Setup add to crib button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        add_crib_behavior = lambda : self.add_crib_check()
        crib_button = GenericButton(behavior=add_crib_behavior,
                                    text="Add to Crib",
                                    width=150,
                                    height=50)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=crib_button,
                align_x = -250,
                align_y = -250)
        )

    def on_show(self):
        self.set_our_hand()
        self.set_other_hand()

    def on_draw(self):
        """
        The on_draw method draws the components of the game every frame
        """

        self.clear()
        self.draw_deck()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()
        self.manager.draw()
        self.draw_tips()

        # Animate other cards
        if self.added_to_crib:
            self.card_animation(self.cards_to_crib)

        if self.can_transition():
            self.make_transition()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks.
        Clicking a card from your hand selects it to be added to the crib.
        Clicking the crib button adds the cards to the crib.
        """

        #if self.game_info.is_turn:
        # Get card object sprites
        card_sprites = arcade.SpriteList()
        for card in self.game_info.our_hand:
            card_sprites.append(card.sprite)

        # Retrieve all cards pressed at the given location
        cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

        # As long as a card was pressed
        if len(cards_pressed) > 0 and self.added_to_crib == False:
            # Retrieve the top card of the cards at the given location
            card = self.game_info.our_hand[card_sprites.index(cards_pressed[-1])]

            # Handle logic of card clicking
            if card not in self.cards_clicked:
                if len(self.cards_clicked) <= 1:
                    self.cards_clicked.append(card)
                    print("Card Picked: ", card.getSuit(), card.getRank())
                else:
                    print("Maximum Number of Cards Already Selected")
            else:
                self.cards_clicked.remove(card)
                print("Card Unpicked: ", card.getSuit(), card.getRank())

            # Modify tip string to help user know what to do next
            match len(self.cards_clicked):
                    case 0:
                        self.tip_string = "Choose a two cards to add to the crib"
                    case 1:
                        self.tip_string = "Choose another card to add to the crib"
                    case 2:
                        self.tip_string = "Click add to crib to add your cards to the crib"


    def on_hide_view(self):
        self.manager.disable()


    def add_crib_check(self):
        """
        Method to verify enough cards were selected for the crib.
        Calls transition if true and displays message if not.
        """
        if len(self.cards_clicked) >= 2:
            print("Cards Added To Crib: ")
            for card in self.cards_clicked:
                print(" ", card.getSuit(), card.getRank())
            # Back end transition call
            # self.transition.add_crib_to_cut_deck(self.game_info, self.cards_clicked[0], self.cards_clicked[1])
            self.added_to_crib = True
            self.cards_to_crib = self.cards_clicked
            self.cards_clicked = []
            self.update_db(cards= self.cards_to_crib)

        else: 
            print("Not enough Cards picked")


    def update_db(self, cards):
        if self.game_info.is_multiplayer:
            self.other_player.add_to_cribbage(game_info, cards)
            

    def can_transition(self):
        if len(self.cards_to_crib) == 2:
            for card in self.cards_to_crib:
                if card.is_animating:
                    return False
            return True
        return False

    def make_transition(self):
        self.transition.pick_crib_transition(
            cards= self.cards_to_crib,
            game_info=self.game_info
        )

    #                   Animations
    #===================================================#
    def card_animation(self, cards):
        for card in cards:
            card.get_dealt_animation(end_position= self.crib_location)