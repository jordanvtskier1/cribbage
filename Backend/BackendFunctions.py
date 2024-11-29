from Card import Card
from GameStates.GameInfo import GameInfo
import random
from itertools import combinations


class Backend:

    def __init__(self):
        pass

    @staticmethod
    def check_game_over(game_info:GameInfo):
        if game_info.our_score >= 121:
            game_info.our_win = True
        if game_info.other_score >= 121:
            game_info.other_score = True
        return game_info


    @staticmethod
    def set_up_next_round(game_info:GameInfo):
        game_info.reset()
        game_info.is_dealer = not game_info.is_dealer
        if game_info.is_dealer:
            Backend.create_deck(game_info)

    @staticmethod
    def create_deck(game_info: GameInfo):
        SUITS = game_info.SUITS
        CARD_VALUES = game_info.CARD_VALUES
        game_info.deck = []
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
            for c in game_info.other_hand:
                if c.suit == card.suit and c.rank == card.rank:
                    game_info.other_hand.remove(c)
                    break

    @staticmethod
    def cut_deck(game_info: GameInfo, card: Card):
        game_info.top_card = card
        for c in game_info.deck:
                if c.suit == card.suit and c.rank == card.rank:
                    game_info.deck.remove(c)
                    break
        game_info.deck.append(card)
        return game_info
    
    @staticmethod
    def calculate_hand_score(game_info: GameInfo, hand):

        hand_score = 0

        complete_hand = list(hand)
        complete_hand.append(game_info.top_card)

        # one for his nob
        top_card = game_info.top_card
        if Card(top_card.getSuit(), "J") in hand:
            hand_score += 1


        # fifteen
        for r in range(2, 6):  # 2 to 5 card combinations
            for combo in combinations(complete_hand, r):
                if sum(card.getValue() for card in combo) == 15:
                    hand_score += 2


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
                hand_score += 2
            if value == 3:
                hand_score += 6
            if value == 4:
                hand_score += 12

        # run of three or more cards
        card_ranks = sorted([card.getRankAsInt() for card in complete_hand])
        # Check for 3, 4, and 5 card runs
        for r in range(3, 6):
            for combo in combinations(card_ranks, r):
                if list(combo) == list(range(combo[0], combo[0] + r)):
                    hand_score += r  # Runs score the number of cards in them

        
        #flush
        suit_duplicates = {}
        for card in hand:
            try:
                #item exists in dict, increment count by 1
                suit_duplicates[card.getSuit()] += 1
            except KeyError:
                #item does not exist in list, make count = 1
                suit_duplicates[card.getSuit()] = 1
        
        for key, value in suit_duplicates.items():
            if value == 4:
                hand_score += 4
                if key == game_info.top_card.getSuit():
                    hand_score += 1

       
        return hand_score

    @staticmethod
    def play_card(game_info: GameInfo, card: Card):
        play_score = 0
        card_sum = sum(card.getValue() for card in game_info.cards_in_play)
        game_info.current_count = card_sum + card.getValue()
        #fifteen
        if card_sum + card.getValue() == 15:
            play_score += 2
        #31
        if card_sum + card.getValue() == 31:
            play_score += 2

         # Pair, triple, and quad
        if len(game_info.cards_in_play) >= 1 and game_info.cards_in_play[-1].getRank() == card.getRank():
            # Triple
            if len(game_info.cards_in_play) >= 2 and game_info.cards_in_play[-2].getRank() == card.getRank():
                # Quad
                if len(game_info.cards_in_play) >= 3 and game_info.cards_in_play[-3].getRank() == card.getRank():
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

        crib_score = 0

        complete_crib = list(game_info.crib)
        complete_crib.append(game_info.top_card)

        # one for his nob
        top_card = game_info.top_card
        if Card(top_card.getSuit(), "J") in game_info.crib:
            crib_score += 1


        # fifteen
        for r in range(2, 6):  # 2 to 5 card combinations
            for combo in combinations(complete_crib, r):
                if sum(card.getValue() for card in combo) == 15:
                    crib_score += 2


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
                crib_score += 2
            if value == 3:
                crib_score += 6
            if value == 4:
                crib_score += 12

        # run of three or more cards
        card_ranks = sorted([card.getRankAsInt() for card in complete_crib])
        # Check for 3, 4, and 5 card runs
        for r in range(3, 6):
            for combo in combinations(card_ranks, r):
                if list(combo) == list(range(combo[0], combo[0] + r)):
                    crib_score += r  # Runs score the number of cards in them

        
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
                    crib_score += 5

       
        return crib_score

    
    @staticmethod
    def can_play_card(game_info: GameInfo, card):

        max_in_play_sum = 31

        card_sum = sum(card.getValue() for card in game_info.cards_in_play)
        return card.getValue() + card_sum <= max_in_play_sum





