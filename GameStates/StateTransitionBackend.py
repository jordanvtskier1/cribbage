
from GameStates.GameInfo import GameInfo
from Game import Game


class StateTransitionBackend:
    def __init__(self, window):
        self.window = window

    # old code
    # @staticmethod
    # def deal_to_add_to_crib(self, game_state: GameState ):
    #
    #     game_info = game_state.gameInfo
    #     # Back end logic of shuffling
    #     game_info.deck = Backend.shuffle_deck()
    #     game_info.has_crib = False
    #     game_info.cards_in_play = []
    #     game_info.is_turn = True
    #     game_info.our_hand = Backend.giveCards(game_info.deck)
    #     game_info.other_hand = Backend.giveCards(game_info.deck)
    #
    #     # State transition
    #     new_state = AddToCribState(game_info)
    #
    #     return new_state

    def menu_to_pick_card(self, game_info: GameInfo):
        from GameStates.PickCardView import PickCardView
        # Backend logic goes here if any

        Game.create_deck(game_info)
        #
        pick_card_view = PickCardView(game_info)
        self.window.show_view(pick_card_view)

    def pick_card_to_add_crib(self, game_info, card):  
        from GameStates.AddToCribView import AddToCribView
        # Backend logic goes here if any
        Game.deal_hands(game_info)
        #
        add_to_crib_view = AddToCribView(game_info)
        self.window.show_view(add_to_crib_view)

    def add_crib_to_cut_deck(self, game_info: GameInfo, cards):
        from GameStates.CutDeckView import CutDeckView
        # Backend logic goes here if any
        indexes = []
        for card in cards:
            indexes.append(game_info.our_hand.index(card))

        Game.send_to_crib(game_info= game_info, hand_indexes= indexes)
        #
        cut_deck_view = CutDeckView(game_info)
        self.window.show_view(cut_deck_view)

    def cut_deck_to_play(self, game_info):
        # Backend logic goes here if any

        #
        pass