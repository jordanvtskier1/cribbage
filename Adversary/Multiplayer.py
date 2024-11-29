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
        while not deal_dict.get(game_info.player, {}).get("hand"):
            pass  # Busy-wait until card data is set

        deck_data = deal_dict.get('deck')
        game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]

        game_info.our_hand = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in
                              deal_dict.get(game_info.player).get("hand")]
        game_info.other_hand = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in
                                deal_dict.get(game_info.opponent).get("hand")]

    def send_deal(self, game_info: GameInfo):
        self.database_ref.update({
            'deck': [card.getDict() for card in game_info.deck],
            game_info.player: {'hand': [card.getDict() for card in game_info.our_hand]},
            game_info.opponent: {'hand': [card.getDict() for card in game_info.other_hand]}
        })

    def send_cut(self, card):
        self.database_ref.update({
            'cut_card': card.getDict()
        })

    def send_play(self, game_info: GameInfo, card: Card):
        self.database_ref.update({
            game_info.player: {'played_card': card.getDict()},
        })

    # send crib picks to databse
    def add_to_cribbage(self, game_info: GameInfo, cards):
        self.database_ref.update({
            game_info.player: {'hand': [card.getDict() for card in game_info.our_hand],
                               'crib_picks': [card.getDict() for card in cards]}
        })

    def cut_deck(self, game_info: GameInfo):
        card_dict = self.listen_get_cards("cut_card", game_info)
        return Card(card_dict["suit"], card_dict["rank"])

    # TODO: change so that we get player hand and cards in play
    def play_card(self, game_info: GameInfo):
        card_dict = self.listen_get_cards(game_info.opponent + "/played_card", game_info)
        return Card(card_dict["suit"], card_dict["rank"])

    def create_game(self, game_info: GameInfo, game_name: str):

        self.database_ref.child(game_name).set("")

        self.database_ref.update({
            game_name: {'deck': [card.getDict() for card in game_info.deck],
                        game_info.player: {'card_pick': ''},
                        game_info.opponent: {'card_pick': ''}}

        })
        self.database_ref = self.database_ref.child(game_name)

    def join_game(self, game_info: GameInfo, game_name: str):

        self.database_ref = self.database_ref.child(game_name)
        game_data = self.database_ref.get()

        if game_data is None:
            pass
        else:
            game_data = self.database_ref.get()
            # Retrieve and convert deck data
            deck_data = game_data.get('deck')
            game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]

    # @staticmethod
    def listen_get_cards(self, path, game_info):
        time.sleep(1)
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

        initial_data = None
        # We do not want old data for played card because it will be the card from last turn
        if path != game_info.opponent + "/played_card":
            initial_data = self.database_ref.child(path).get()

        if initial_data is not None:
            print(f"initial data: {initial_data}")
            card_dict = initial_data
        else:
            listener = self.database_ref.child(path).listen(on_card_pick_change)

            # Wait until data is captured
            while not card_dict:
                pass  # Busy-wait until card data is

        return card_dict

    #     These functions are called on the views instead
    # ===========================================================#
    # Listen for opponents card pick
    def pick_card(self, view):
        def get_picked_card(event):
            print(event.event_type)  # can be 'put' or 'patch'
            print(event.path)  # relative to the reference, it seems
            print(event.data)  # new data at /reference/event.path. None if deleted

            if event.data != '' and event.data is not None:
                view.other_card = Card(event.data["suit"], event.data["rank"])

                # Play animation
                view.animate_other_card()
                try:
                    listener.close()
                except:
                    pass

        listener = self.database_ref.child(view.game_info.opponent + "/card_pick").listen(get_picked_card)

    def send_pick_card(self, game_info: GameInfo, card: Card):
        query = {
            game_info.player: {'card_pick': card.getDict()}
        }
        self.database_ref.update(query)

    def listen_to_deal(self, view):
        deal_dict = {}
        player = view.game_info.player
        opponent = view.game_info.opponent

        # Callback function to capture data change
        def on_deal_change(event):
            nonlocal deal_dict
            if event.data is not None:
                print(f"Data: {event.data}")
                deal_dict = event.data
                view.listener_done = True

                Multiplayer.assign_deal(game_info=view.game_info, deal_dict=deal_dict)

                # Stop listening after the first change is captured
                try:
                    listener.close()
                except:
                    pass

        listener = self.database_ref.listen(on_deal_change)

    def listen_to_play(self, view):
        def get_played_card(event):
            print(event.data)  # new data at /reference/event.path. None if deleted

            if event.data != '' and event.data is not None:
                played_card = Card(event.data["suit"], event.data["rank"])

                view.card_was_played(card=played_card)
                # Delete from database so we don't read it again next turn
                self.database_ref.child(view.game_info.opponent + "/played_card").delete()
                try:
                    listener.close()
                except:
                    pass

        listener = self.database_ref.child(view.game_info.opponent + "/played_card").listen(get_played_card)

    @staticmethod
    def assign_deal(game_info: GameInfo, deal_dict: dict):
        player = game_info.player
        opponent = game_info.opponent

        deck_data = deal_dict.get('deck')
        game_info.deck = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in deck_data]

        game_info.our_hand = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in
                              deal_dict.get(player).get("hand")]
        game_info.other_hand = [Card(card_dict["suit"], card_dict["rank"]) for card_dict in
                                deal_dict.get(opponent).get("hand")]

    def listen_to_cribbage(self, view):

        def get_crib_picks(event):
            print(event.event_type)  # can be 'put' or 'patch'
            print(event.path)  # relative to the reference, it seems
            print(event.data)  # new data at /reference/event.path. None if deleted

            if event.data is not None:
                cards = []

                for card_dict in event.data:
                    view.other_picks.append(
                        Card(
                            card_dict["suit"],
                            card_dict["rank"]
                        )
                    )

                # Play animation
                # view.animate_other_card()
                try:
                    view.listener_done = True
                    listener.close()
                except:
                    pass

        listener = self.database_ref.child(view.game_info.opponent + "/crib_picks").listen(get_crib_picks)

    def listen_to_cut(self, view):
        path = "cut_card"

        # Callback function to capture data change
        def listen_to_event(event):
            print(event.event_type)  # can be 'put' or 'patch'
            print(event.path)  # relative to the reference, it seems
            print(event.data)  # new data at /reference/event.path. None if deleted

            if event.data is not None:
                view.listener_done = True

                view.picked_card = Card(
                    event.data["suit"],
                    event.data["rank"]
                )

                # Stop listening after the first change is captured
                try:
                    listener.close()
                except:
                    pass

        listener = self.database_ref.child(path).listen(listen_to_event)

