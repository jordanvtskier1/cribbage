
from GameStates.GameInfo import GameInfo
from Backend.BackendFunctions import Backend
from Card import Card
from Connection.config import init
import json



class StateTransitionBackend:
    def __init__(self, window):
        self.window = window
        self.database_ref = init()
        # player1 or player2
        self.player = ""

    def create_game_to_pick_card(self, game_info: GameInfo, game_name):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)
        self.player = "player1"
        self.database_ref.set({
            'deck': [card.getDict() for card in game_info.deck],
            'game_name': game_name
        })

        #pick_card_view = PickCardView(game_info)
        #self.window.show_view(pick_card_view)
    
    def join_game_to_pick_card(self, game_info: GameInfo, game_name): 
        from GameStates.PickCardView import PickCardView

        self.player = "player2"

        game_data = self.database_ref.get().val()
        if game_data:
            # Retrieve and convert deck data
            deck_data = game_data.get('deck')
            game_info.deck = [Card.fromDict(card_dict) for card_dict in deck_data]  # Assuming a Card.fromDict method
            game_info.game_name = game_data.get('game_name')

        #pick_card_view = PickCardView(game_info)
        #self.window.show_view(pick_card_view)

    def menu_to_pick_card(self, game_info: GameInfo):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)
        
        pick_card_view = PickCardView(game_info)
        self.window.show_view(pick_card_view)


    def pick_card_to_add_crib(self, game_info, card):
        from GameStates.AddToCribView import AddToCribView
        
        opponent_card = self.get_opponent_card(game_info.game_name, self.player)

        # opponent_card = Firebase.getCard()
        # if card > opponent_card:
            # game_info.is_dealer = False
            # game_info.has_crib = False
        # else:
            # game_info.is_dealer = True
            # game_info.has_crib = True
        game_info = Backend.deal_cards(game_info)

        add_to_crib_view = AddToCribView(game_info)
        self.window.show_view(add_to_crib_view)

    def add_crib_to_cut_deck(self, game_info: GameInfo, card1, card2):
        from GameStates.CutDeckView import CutDeckView
        # Backend logic goes here if any

        game_info = Backend.add_to_crib(game_info, card1, card2)

        # opponent_cards = Firebase.get_crib_picks()
        # game_info = Backend.add_to_crib(game_info, opponent_cards)
        
        cut_deck_view = CutDeckView(game_info)
        self.window.show_view(cut_deck_view)

    def cut_deck_to_play(self, game_info, card):
        from GameStates.PlayView import PlayView
        
        game_info = Backend.cut_deck(game_info, card)

        # Calculate hand score
        game_info = Backend.calculate_hand_score(game_info)

        # opponent_score = Firebase.getOppScore()
        # game_info.other_score = opponent_score
        
        play_view = PlayView(game_info)
        self.window.show_view(play_view)

    def play_to_wait(self, game_info: GameInfo, card: Card):
        from GameStates.PlayView import PlayView
        from GameStates.WaitView import WaitView

        played_card_sum = sum(card.getValue() for card in game_info.cards_in_play)
    
        if sum(played_card_sum, card.getValue()) > 31:
            game_info.is_turn = False
            game_info.can_play = False
            play_view = WaitView(game_info)

        else:
            game_info = Backend.play_card(game_info, card)
            game_info.is_turn = False
            play_view = PlayView(game_info)

        self.window.show_view(play_view)

    def play_to_show_score(self, game_info: GameInfo):
        from GameStates.ShowScoreView import ShowScoreView
        self.window.show_view(ShowScoreView(game_info))

    def show_score_to_crib(self, game_info: GameInfo):
        from GameStates.AddToCribView import AddToCribView

        Game.create_deck(game_info)
        Game.deal_hands(game_info)

        self.window.show_view(AddToCribView(game_info))