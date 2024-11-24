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



    def add_to_cribbage(self, game_info: GameInfo):
        card_indexes = random.sample(range(len(game_info.other_hand)), 2)
        return [game_info.other_hand[card_indexes[0]], game_info.other_hand[card_indexes[1]]]

    def cut_deck(self, game_info: GameInfo):
        # Randomly select a card from the deck
        deck_size = len(game_info.deck)
        card_index = random.randint(0, deck_size - 1)
        cut_card = game_info.deck[card_index]  

        print(f"CPU cut card: {cut_card}")
        return cut_card

    def play_card(self, game_info: GameInfo):
        card_index = random.randint(0, len(game_info.other_hand) - 1)
        card = game_info.other_hand[card_index]
        return card