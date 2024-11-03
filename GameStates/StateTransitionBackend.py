from GameStates.GameInfo import GameInfo
from GameStates.GameState import GameState
from GameStates.AddToCribState import AddToCribState
from GameStates.PickCardView import PickCardView
from Card import Card



class StateTransitionBackend:
    def __init__(self):
        pass

    def menu_to_pick_card(self, game_info: GameInfo, card: Card):
        #return PickCardView(game_info)
        pass
    
    def pick_card_to_crib(self, game_info: GameInfo, card: Card):
        #return AddCribView(game_info)
        pass

    @staticmethod
    def deal_to_add_to_crib(self, game_state: GameState ):

        game_info = game_state.gameInfo
        # Back end logic of shuffling
        game_info.deck = Backend.shuffle_deck()
        game_info.has_crib = False
        game_info.cards_in_play = []
        game_info.is_turn = True
        game_info.our_hand = Backend.giveCards(game_info.deck)
        game_info.other_hand = Backend.giveCards(game_info.deck)

        # State transition
        new_state = AddToCribState(game_info)

        return new_state