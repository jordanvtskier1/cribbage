from Adversary.OtherPlayerLogic import OtherPlayerLogic
from GameStates.GameInfo import GameInfo
from Backend.BackendFunctions import Backend
from Card import Card
from Connection.config import init
import json
import firebase_admin
import threading
import arcade



class StateTransitionBackend:
    def __init__(self, window: arcade.Window):
        self.window = window
        self.database_ref = init()
        
        

    def create_game_to_pick_card(self, game_info: GameInfo, game_name):
        from GameStates.PickCardView import PickCardView

        #clear game with same name if it exists
        self.database_ref.child(game_name).set("")


        game_info = Backend.create_deck(game_info)
        self.player = "player1"
        self.opponent = "player2"
        self.database_ref.update({
            game_name: {'deck': [card.getDict() for card in game_info.deck],
                        self.player: {'card_pick': ''},
                        self.opponent: {'card_pick': ''}}

        })

        self.database_ref = self.database_ref.child(game_name)

        pick_card_view = PickCardView(game_info, self)
        self.window.show_view(pick_card_view)
    
    def join_game_to_pick_card(self, game_info: GameInfo, game_name: str): 
        from GameStates.PickCardView import PickCardView

        self.player = "player2"
        self.opponent = "player1"
        self.database_ref = self.database_ref.child(game_name)

        game_data = self.database_ref.get()
        if game_data is None:
            raise ValueError(f"The Game {game_name} does not exist.")


        # Retrieve and convert deck data
        deck_data = game_data.get('deck')
        game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]  # Assuming a Card.fromDict method
        #game_info.game_name = game_data.get('game_name')
        for card in game_info.deck:
            print(card)

        pick_card_view = PickCardView(game_info, state_transition=self)
        self.window.show_view(pick_card_view)

    '''def menu_to_pick_card(self, game_info: GameInfo):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)
        
        pick_card_view = PickCardView(game_info, state_transition= self)
        self.window.show_view(pick_card_view)'''


    def pick_card_to_add_crib(self, game_info: GameInfo, card: Card):
        from GameStates.AddToCribView import AddToCribView
        from GameStates.PickCardView import PickCardView
        
        query = {
            self.player: {'card_pick': card.getDict()}
        }
        self.database_ref.update(query)

        card_dict = {}


        # Callback function to capture data change
        def on_card_pick_change(event):
            nonlocal card_dict
            print(f"Data change detected at {event.path}")
            if event.data:
                print(f"Data: {event.data}")
                card_dict = event.data
                # Stop listening after the first change is captured
                try:
                    listener.close()
                except:
                    pass

        initial_data = self.database_ref.child(self.opponent+"/card_pick").get()

        if initial_data:
            print(f"initial data: {initial_data}")
            card_dict = initial_data
        else:
            listener = self.database_ref.child(self.opponent+"/card_pick").listen(on_card_pick_change)
            #listener = self.database_ref.listen(on_card_pick_change)

            # Wait until data is captured
            while not card_dict:
                pass  # Busy-wait until card data is set

        opponent_card = Card(card_dict["suit"], card_dict["rank"])


        if card > opponent_card:
            game_info.is_dealer = False

            deal_dict = {}

            # Callback function to capture data change
            def on_deal_change(event):
                nonlocal deal_dict
                if event.data:
                    print(f"Data: {event.data}")
                    deal_dict = event.data
                    # Stop listening after the first change is captured
                    try:
                        listener.close()
                    except:
                        pass
            
            listener = self.database_ref.listen(on_deal_change)

            # Wait until data is captured
            while not deal_dict:
                pass  # Busy-wait until card data is set

            deck_data = deal_dict.get('deck')
            game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]

            game_info.our_hand = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deal_dict.get(self.player).get("hand")]
            game_info.other_hand = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deal_dict.get(self.opponent).get("hand")]


            add_to_crib_view = AddToCribView(game_info, state_transition= self)
            self.window.show_view(add_to_crib_view)

        elif card < opponent_card:
            game_info.is_dealer = True
            game_info = Backend.deal_cards(game_info)

            self.database_ref.update({
            'deck': [card.getDict() for card in game_info.deck],
            self.player: {'hand': [card.getDict() for card in game_info.our_hand]},
            self.opponent:  {'hand': [card.getDict() for card in game_info.other_hand]}
            })

            add_to_crib_view = AddToCribView(game_info, state_transition= self)
            self.window.show_view(add_to_crib_view)

        elif card==opponent_card:
            view = PickCardView(game_info, state_transition=self)
            self.window.show_view(view)

        
        

        
        

    def add_crib_to_cut_deck(self, game_info: GameInfo, card1, card2):
        from GameStates.CutDeckView import CutDeckView
        # Backend logic goes here if any

        Backend.add_to_crib(game_info, card1, card2)
        Backend.remove_from_our_hand(game_info, [card1, card2])

        # opponent_cards = Firebase.get_crib_picks()
        opponent_cards = self.other_player.add_to_cribbage(game_info)

        Backend.add_to_crib(game_info, opponent_cards[0], opponent_cards[1])
        Backend.remove_from_other_hand(game_info, [opponent_cards[0],  opponent_cards[1]])
        
        cut_deck_view = CutDeckView(game_info, state_transition= self)
        self.window.show_view(cut_deck_view)

    def cut_deck_to_play(self, game_info, card):
        from GameStates.PlayView import PlayView

        # We should pass none if we dont want to cut the deck
        if card is None:
            card = self.other_player.cut_deck(game_info)

        game_info = Backend.cut_deck(game_info, card)
        
        play_view = PlayView(game_info, state_transition= self)
        self.window.show_view(play_view)


    def play_to_wait(self, game_info: GameInfo, card: Card):
        from GameStates.PlayView import PlayView
        #from GameStates.WaitView import WaitView

        #When it is not our turn
        if card is None or game_info.is_turn is False:
            other_card = self.other_player.play_card(game_info)
            #TODO add backend logic for playing cards ? I dont know how it works
            game_info.cards_in_play.append(other_card)
            game_info.other_hand.remove(other_card)
            game_info.is_turn = True

        else:
            played_card_sum = sum(card.getValue() for card in game_info.cards_in_play)

            if played_card_sum + card.getValue() > 31:
                game_info.can_play = False
                #TODO add output message

            else:
                game_info = Backend.play_card(game_info, card)

            game_info.is_turn = False
        play_view = PlayView(game_info, state_transition= self)

        self.window.show_view(play_view)

    def play_to_show_score(self, game_info: GameInfo):
        from GameStates.ShowScoreView import ShowScoreView
        # Calculate hand score
        game_info = Backend.calculate_hand_score(game_info)

        # opponent_score = Firebase.getOppScore()
        # game_info.other_score = opponent_score
        self.window.show_view(ShowScoreView(game_info))

    def show_score_to_crib(self, game_info: GameInfo):
        from GameStates.AddToCribView import AddToCribView

        game_info.reset()
        Backend.create_deck(game_info)
        Backend.deal_cards(game_info)

        self.window.show_view(AddToCribView(game_info, state_transition= self))


