from Card import Card
from GameStates.GameInfo import GameInfo
import random
from itertools import combinations


class Backend:

    def __init__(self):
        pass

    @staticmethod
    def create_deck(game_info: GameInfo):
        SUITS = game_info.SUITS
        CARD_VALUES = game_info.CARD_VALUES
        for suit in SUITS: 
            for value in CARD_VALUES: 
                game_info.deck.append(Card(suit, value))
        random.shuffle(game_info.deck)
        return game_info
    
    
    @staticmethod
    def deal_cards(game_info: GameInfo):
        DEAL = game_info.DEAL
        for index in range(0, DEAL):
            game_info.our_hand.append(game_info.deck.pop(0))
            game_info.other_hand.append(game_info.deck.pop(0))
        return game_info
    
    @staticmethod
    def add_to_crib(game_info: GameInfo, cards: list[Card]):
        for card in cards:
            game_info.crib.append(card)
        return

    @staticmethod
    def remove_from_our_hand(game_info: GameInfo, cards: list[Card]):
        for card in cards:
            game_info.our_hand.remove(card)

    @staticmethod
    def remove_from_other_hand(game_info: GameInfo, cards):
        for card in cards:
            game_info.other_hand.remove(card)

    @staticmethod
    def cut_deck(game_info: GameInfo, card: Card):
        game_info.top_card = card
        game_info.deck.remove(card)
        game_info.deck.append(card)
        return game_info
    
    @staticmethod
    def calculate_hand_score(game_info: GameInfo):

        complete_hand = game_info.our_hand
        complete_hand.append(game_info.top_card)

        # one for his nob
        top_card = game_info.top_card
        if Card(top_card.getSuit(), "J") in game_info.our_hand:
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
    def play_card(game_info: GameInfo, card: Card):
        play_score = 0
        card_sum = sum(card.getValue() for card in game_info.cards_in_play)
        #fifteen
        if card_sum == 15:
            play_score += 2
        #31
        if card_sum == 31:
            play_score += 2

         # Pair, triple, and quad
        if len(game_info.cards_in_play) >= 2 and game_info.cards_in_play[-2].getRank() == card.getRank():
            # Triple
            if len(game_info.cards_in_play) >= 3 and game_info.cards_in_play[-3].getRank() == card.getRank():
                # Quad
                if len(game_info.cards_in_play) >= 4 and game_info.cards_in_play[-4].getRank() == card.getRank():
                    play_score += 12  # Quad score (quadruple, 4 cards)
                else:
                    play_score += 6  # Triple score
            else:
                play_score += 2  # Pair score

        # Run
        run_length = 1
        sorted_ranks = sorted(card.getRankAsInt() for card in game_info.cards_in_play[-5:])  # Last 5 cards
        for i in range(len(sorted_ranks) - 1):
            if sorted_ranks[i] + 1 == sorted_ranks[i + 1]:  # Check if consecutive
                run_length += 1
            else:
                run_length = 1  # Reset if sequence is broken
            
            if run_length >= 3:
                play_score += run_length  # Add score for the run length

        return play_score

    @staticmethod
    def calculate_crib_score(game_info: GameInfo):

        complete_crib = game_info.crib.append(game_info.top_card)

        # one for his nob
        top_card = game_info.top_card
        if Card(top_card.getSuit(), "J") in game_info.crib:
            game_info.crib_score += 1


        # fifteen
        for r in range(2, 6):  # 2 to 5 card combinations
            for combo in combinations(complete_crib, r):
                if sum(card.getValue() for card in combo) == 15:
                    game_info.crib_score += 2


        # counts of cards in hand
        rank_duplicates = {}
        for card in complete_crib:
            try:
                #item exists in dict, increment count by 1
                rank_duplicates[card.getRank()] += 1
            except KeyError:
                #item does not exist in list, make count = 1
                rank_duplicates[card.getRank()] = 1

        # pairs, 3-of-kind, 4-of-kind
        for key, value in rank_duplicates.items():
            if value == 2:
                game_info.crib_score += 2
            if value == 3:
                game_info.crib_score += 6
            if value == 4:
                game_info.crib_score += 12

        # run of three or more cards
        card_ranks = sorted([card.getRankAsInt() for card in complete_crib])
        # Check for 3, 4, and 5 card runs
        for r in range(3, 6):
            for combo in combinations(card_ranks, r):
                if list(combo) == list(range(combo[0], combo[0] + r)):
                    game_info.crib_score += r  # Runs score the number of cards in them

        
        #flush of 5
        suit_duplicates = {}
        for card in game_info.crib:
            try:
                #item exists in dict, increment count by 1
                suit_duplicates[card.getSuit()] += 1
            except KeyError:
                #item does not exist in list, make count = 1
                suit_duplicates[card.getSuit()] = 1
        
        for key, value in suit_duplicates.items():
            if value == 4:
                if key == game_info.top_card.getSuit():
                    game_info.crib_score += 5

       
        return game_info

    






