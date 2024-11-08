# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game


import arcade
from GameStates import GameInfo
from GameStates.GameView import GameView
from GUI.Buttons.GenericButton import GenericButton
import arcade.gui


class AddToCribView(GameView):
    """Class representing the adding cards to the crib portion of the game"""

    def __init__(self, game_info: GameInfo):
        super().__init__(game_info)

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


    def on_mouse_press(self, x, y, button, modifiers):
        """
        The on_mouse_press method takes in mouse clicks and performs an action based on those clicks.
        Clicking a card from your hand selects it to be added to the crib.
        Clicking the crib button adds the cards to the crib.
        """

        if self.game_info.is_turn:
            # Get card object sprites
            card_sprites = arcade.SpriteList()
            for card in self.game_info.our_hand:
                card_sprites.append(card.sprite)

            # Retrieve all cards pressed at the given location
            cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

            # As long as a card was pressed
            if len(cards_pressed) > 0:
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
            self.transition.add_crib_to_cut_deck(self.game_info, self.cards_clicked[0], self.cards_clicked[1])
        else: 
            print("Not enough Cards picked")

    def draw_tips(self):
        """
        The draw_tips method draws the tips for the player to help them understand the game
        """
        arcade.draw_rectangle_filled(self.YOUR_HAND_LOCATION[0] + 150, self.YOUR_HAND_LOCATION[1] + 100, 350, 30, arcade.color.LIGHT_GRAY)
        arcade.draw_text(self.tip_string, self.YOUR_HAND_LOCATION[0] - 20, self.YOUR_HAND_LOCATION[1] + 93, arcade.color.BLACK, 10)
