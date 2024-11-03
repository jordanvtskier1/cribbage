from GameStates.PickCardView import PickCardView



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

    def menu_to_cut_deck(self, game_info):
        # Backend logic goes here if any

        #
        pick_card_view = PickCardView(game_info)
        self.window.show_view(pick_card_view)