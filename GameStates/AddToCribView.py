# View for adding cards to the crib
# CS 3050: Software Engineering
# Final Project: Cribbage Game

# Import required files and modules
import arcade
from GameStates import GameInfo
from GameStates.StateTransitionBackend import StateTransitionBackend
from GameStates.GameView import GameView
from GameStates.CutDeckView import CutDeckView

# AddToCribView inherits from GameView so that it can use all its methods
# NOTE: Now inherits from GameView. Benefits: Gets all of GameViews variables and methods
class AddToCribView(GameView):
    
    def __init__(self, game_info: GameInfo):
        # Call parent constructor
        super().__init__(game_info)


    def on_draw(self):
        self.clear()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_pegs()
        self.draw_deck()
        self.draw_our_hand()
        self.draw_other_hand()
        self.draw_crib()
        self.draw_crib_button()


    def on_mouse_press(self, x, y, button, modifiers):

        if self.game_info.is_turn:
            card_sprites = arcade.SpriteList()
            for card in self.game_info.our_hand:
                card_sprites.append(card.sprite)
            # Retrieve all cards pressed at the given location
            cards_pressed = arcade.get_sprites_at_point((x, y), card_sprites)

            # As long as a card was pressed
            if len(cards_pressed) > 0:
                # Adjust the game state so that the card pressed is moved to the center of play
                card = self.game_info.our_hand[card_sprites.index(cards_pressed[-1])]
                if card not in self.cards_clicked:
                    if len(self.cards_clicked) <= 1:
                        self.cards_clicked.append(card)
                        print("Card Picked: ", card.getSuit(), card.getRank())
                    else:
                        print("Maximum Number of Cards Already Selected")
                else:
                    self.cards_clicked.remove(card)
                    print("Card Unpicked: ", card.getSuit(), card.getRank())
            if 35 <= y <= 85 and 175 <= x <= 325:
                if len(self.cards_clicked) >= 2:
                    print("Cards Added To Crib: ")
                    for card in self.cards_clicked:
                        print(" ", card.getSuit(), card.getRank())
                    # Back end transition call
                    self.transition.add_crib_to_cut_deck(self.game_info, self.cards_clicked[0], self.cards_clicked[1])
                else: 
                    print("Not enough Cards picked")


    def draw_crib_button(self):
        # Draws the deal button
        arcade.draw_rectangle_filled(250, 60, 150, 25, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Add Cards To Crib", 190, 55, arcade.color.BLACK, 11)
        