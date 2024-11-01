from Card import Card
from GameStates.GameInfo import GameInfo
import random
from itertools import combinations


class Backend:

    def __init__(self):
        pass

    @staticmethod
    def deal_cards(game_info: GameInfo):
        SUITS = game_info.SUITS
        CARD_VALUES = game_info.CARD_VALUES
        for suit in SUITS: 
            for value in CARD_VALUES: 
                game_info.deck.append(Card(suit, value))
        game_info.deck = random.shuffle(game_info.deck)
        return game_info
    
    def add_to_crib(game_info: GameInfo, card1: Card, card2: Card):
        game_info.crib.append(card1)
        game_info.crib.append(card2)
        game_info.our_hand.remove(card1)
        game_info.our_hand.remove(card2)
        return game_info
    
    @staticmethod
    def calculate_hand_score(game_info: GameInfo):

        complete_hand = game_info.our_hand.append(game_info.top_card[0])

        # one for his nob
        top_card = game_info.top_card[0]
        if Card(top_card.getSuit(), "Jack") in game_info.our_hand:
            game_info.our_score += 1


        # fifteen
        for r in range(2, 6):  # 2 to 5 card combinations
            for combo in combinations(complete_hand, r):
                if sum(card.getValue() for card in combo) == 15:
                    game_info.our_score += 2


        # counts of cards in hand
        rank_duplicates = {}
        for card in complete_hand:
            try:
                #item exists in dict, increment count by 1
                rank_duplicates[card.getRank()] += 1
            except KeyError:
                #item does not exist in list, make count = 1
                rank_duplicates[card.getRank()] = 1

        # pairs, 3-of-kind, 4-of-kind
        for key, value in rank_duplicates.items():
            if value == 2:
                game_info.our_score += 2
            if value == 3:
                game_info.our_score += 6
            if value == 4:
                game_info.our_score += 12

        # run of three or more cards
        card_ranks = sorted([card.getRankAsInt() for card in complete_hand])
        # Check for 3, 4, and 5 card runs
        for r in range(3, 6):
            for combo in combinations(card_ranks, r):
                if list(combo) == list(range(combo[0], combo[0] + r)):
                    game_info.our_score += r  # Runs score the number of cards in them

        
        #flush
        suit_duplicates = {}
        for card in game_info.our_hand:
            try:
                #item exists in dict, increment count by 1
                suit_duplicates[card.getSuit()] += 1
            except KeyError:
                #item does not exist in list, make count = 1
                suit_duplicates[card.getSuit()] = 1
        
        for key, value in suit_duplicates.items():
            if value == 4:
                game_info.our_score += 4
                if key == game_info.top_card.getSuit():
                    game_info.our_score += 1

       
        return game_info

    @staticmethod
    def take_turn(game_info: GameInfo, card):
        game_info.cards_in_play.append(card)
        game_info.sum(game_info.cards_in_play)
        game_info.our_hand.remove(card) 
        return game_info

        
    






