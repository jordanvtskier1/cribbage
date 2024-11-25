from logging.config import listen

from Adversary.OtherPlayerLogic import OtherPlayerLogic
from GameStates.GameInfo import GameInfo
from Card import Card
import random
from Backend.BackendFunctions import Backend
from threading import Thread
import time

class CPU(OtherPlayerLogic):
    def __init__(self):
        super().__init__()

    # picks card from deck
    @staticmethod
    def pick_card(view):
        t = Thread(target=CPU.pick_card_async, args=[view])
        t.start()

    @staticmethod
    def pick_card_async(view):

        time.sleep(1)

        # Randomly select a card from the deck
        deck_size = len(view.game_info.deck)
        card_index = random.randint(0, deck_size - 1)
        opponent_card = view.game_info.deck[card_index]

        print(f"CPU picked card: {opponent_card}")
        view.other_card = opponent_card
        view.animate_other_card()

    @staticmethod
    def listen_to_deal(view):
        t = Thread(target=CPU.listen_to_deal_async, args=[view])
        t.start()

    @staticmethod
    def listen_to_deal_async(view):
        time.sleep(3)
        game_info = Backend.deal_cards(view.game_info)
        view.listener_done = True

    @staticmethod
    def send_deal(game_info: GameInfo):
        pass

    @staticmethod
    def listen_to_cribbage(view):
        t = Thread(target=CPU.add_to_cribbage_async, args=[view])
        t.start()

    @staticmethod
    def add_to_cribbage_async(view):
        time.sleep(1)
        other_hand = view.game_info.other_hand
        card_indexes = random.sample(range(len(other_hand)), 2)

        cards = [ other_hand[ card_indexes[0]], other_hand[ card_indexes[1]]]
        view.other_picks = cards

        view.listener_done = True

    @staticmethod
    def listen_to_cut(view):
        t = Thread(target=CPU.listen_to_cut_async, args=[view])
        t.start()


    @staticmethod
    def listen_to_cut_async(view):
        time.sleep(2)
        view.picked_card = CPU.cut_deck( game_info = view.game_info )
        view.listener_done = True

    @staticmethod
    def cut_deck(game_info: GameInfo):
        # Randomly select a card from the deck
        deck_size = len(game_info.deck)
        card_index = random.randint(0, deck_size - 1)
        cut_card = game_info.deck[card_index]  

        return cut_card

    @staticmethod
    def listen_to_play(view):
        t = Thread(target=CPU.listen_to_play_async, args=[view])
        t.start()

    @staticmethod
    def listen_to_play_async(view):
        time.sleep(2)
        played_card = CPU.play_card(game_info=view.game_info)
        view.card_was_played(card=played_card)

    """
    We should only play a card if the count would go under 31.
    Otherwise we return no cards
    """
    @staticmethod
    def play_card(game_info: GameInfo):

        pick_range = list( range( len(game_info.other_hand) - 1))

        # Try picks until one works
        while len(pick_range) > 0:
            card_index = random.choice( pick_range )
            card = game_info.other_hand[card_index]

            if Backend.can_play_card(game_info, card):
                return card

            # We cant pick that index
            pick_range.remove( card_index )
        return None
