from Adversary.OtherPlayerLogic import OtherPlayerLogic
from GameStates.GameInfo import GameInfo
from Connection.config import init
from Backend.BackendFunctions import Backend
from Card import Card
import time

class Multiplayer(OtherPlayerLogic):
    def __init__(self):
         super().__init__()
         self.database_ref = init()
         
    # Choosing a card in the pick card state
    def pick_card(self, game_info: GameInfo, card: Card):

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

            # Wait until data is captured
            while not card_dict:
                pass  # Busy-wait until card data is set


        opponent_card = Card(card_dict["suit"], card_dict["rank"])

        # reset card pick in case both players picked same cards and we need to pick again
        query = {
        self.player: {'card_pick': ''}
        }
        self.database_ref.update(query)

        return opponent_card
    
    def get_deal(self, game_info: GameInfo):

        time.sleep(1)

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


    def send_deal(self, game_info: GameInfo):

        self.database_ref.update({
        'deck': [card.getDict() for card in game_info.deck],
        self.player: {'hand': [card.getDict() for card in game_info.our_hand]},
        self.opponent:  {'hand': [card.getDict() for card in game_info.other_hand]}
        })


 

    def add_to_cribbage(self, game_info: GameInfo):
        pass

    def cut_deck(self, game_info: GameInfo):
        pass

    def play_card(self, game_info: GameInfo):
        pass


    def create_game(self, game_info: GameInfo, game_name: str):

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

    def join_game(self, game_info: GameInfo, game_name: str):
        self.player = "player2"
        self.opponent = "player1"
        self.database_ref = self.database_ref.child(game_name)

        game_data = self.database_ref.get()
    
        if game_data is None:
            pass
        
        else:
            game_data = self.database_ref.get()
            # Retrieve and convert deck data
            deck_data = game_data.get('deck')
            game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]
        
