
from GameStates.GameInfo import GameInfo
from Backend.BackendFunctions import Backend
from Card import Card
from Connection.config import init
import json
import firebase_admin
import threading



class StateTransitionBackend:
    def __init__(self, window):
        self.window = window
        '''
        if not firebase_admin._apps:
            self.database_ref = init()
        else:
            self.database_ref = firebase_admin.get_app("my_app")'''
        
        self.database_ref = init()
        

    def create_game_to_pick_card(self, game_info: GameInfo, game_name):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)
        game_info.which_player = "player1"
        game_info.other_player = "player2"
        self.database_ref.update({
            game_name: {'deck': [card.getDict() for card in game_info.deck]}
        })

        self.database_ref = self.database_ref.child(game_name)



        #pick_card_view = PickCardView(game_info)
        #self.window.show_view(pick_card_view)
    
    def join_game_to_pick_card(self, game_info: GameInfo, game_name: str): 
        from GameStates.PickCardView import PickCardView

        game_info.which_player = "player2"
        game_info.other_player = "player1"
        self.database_ref = self.database_ref.child(game_name)

        game_data = self.database_ref.get()#.val()
        if game_data is None:
            raise ValueError(f"The Game {game_name} does not exist.")


        # Retrieve and convert deck data
        deck_data = game_data.get('deck')
        game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]  # Assuming a Card.fromDict method
        #game_info.game_name = game_data.get('game_name')
        for card in game_info.deck:
            print(card)

        #pick_card_view = PickCardView(game_info)
        #self.window.show_view(pick_card_view)

    def menu_to_pick_card(self, game_info: GameInfo):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)
        
        pick_card_view = PickCardView(game_info)
        self.window.show_view(pick_card_view)


    def pick_card_to_add_crib(self, game_info: GameInfo, card: Card):
        from GameStates.AddToCribView import AddToCribView
        
        query = {
            "player1": {'card_pick': card.getDict()}
        }
        print(query)
        """self.database_ref.update({
                    game_info.which_player: {'card_pick': card.getDict()}
                })"""
        self.database_ref.update(query)


        opponent_card = {}
        stop_event = threading.Event()

        # Callback function to capture data change
        def on_card_pick_change(event):
            nonlocal opponent_card
            print("Data change detected at player1/card_pick")
            opponent_card = event.data
            # Stop listening after the first change is captured
            stop_event.set() 

        

        
        listener = self.database_ref.child("player1"+"/card_pick").listen(on_card_pick_change)

        stop_event.wait()
        listener.close()
        # Wait until data is captured
        while not opponent_card:
            pass  # Busy-wait until card data is set

        print(opponent_card)

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