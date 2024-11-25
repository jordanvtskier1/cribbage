from Adversary.OtherPlayerLogic import OtherPlayerLogic
from GameStates.GameInfo import GameInfo
from Backend.BackendFunctions import Backend
from Card import Card
from Connection.config import init
from Adversary.CPU import CPU
from Adversary.Multiplayer import Multiplayer
import json
import firebase_admin
import threading
import arcade
import time


MAX_PLAYABLE_CARDS = 8



class StateTransitionBackend:
    def __init__(self, window: arcade.Window):
        self.window = window
        self.database_ref = init()
        self.other_player = OtherPlayerLogic()

    def set_other_player(self, other_player_logic):
        self.other_player = other_player_logic

    def menu_to_pick_card(self, game_info: GameInfo):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)


        pick_card_view = PickCardView(game_info, state_transition=self)
        self.window.show_view(pick_card_view)


    def create_game_to_pick_card(self, game_info: GameInfo, game_name):
        from GameStates.PickCardView import PickCardView

        self.other_player = Multiplayer()
        game_info.opponent = "player2"
        game_info.player = "player1"
        self.other_player.create_game(game_info=game_info, game_name=game_name)
        pick_card_view = PickCardView(game_info, self)
        self.window.show_view(pick_card_view)


    def join_game_to_pick_card(self, game_info: GameInfo, game_name: str): 
        from GameStates.PickCardView import PickCardView
        from GameStates.MenuViews.JoinInputView import JoinInputView
        

        self.other_player = Multiplayer()
        game_info.opponent = "player1"
        game_info.player = "player2"
        self.other_player.join_game(game_info=game_info, game_name=game_name)

        if not game_info.deck:
             join_game_view = JoinInputView(game_info=game_info, state_transition=self)
             self.window.show_view(join_game_view)

        else:
            pick_card_view = PickCardView(game_info, state_transition=self)
            self.window.show_view(pick_card_view)


    def pick_card_to_add_crib(self, game_info: GameInfo, card: Card, opponent_card: Card):

        from GameStates.PickCardView import PickCardView
        from GameStates.WaitForDealView import WaitForDealView
        from GameStates.AddToCribView import AddToCribView

        # means that both players picked same card, return to pick card view
        if card == opponent_card:
            view = PickCardView(game_info, state_transition=self)
            self.window.show_view(view)
        else:
            if card > opponent_card:
                game_info.is_dealer = False

                # We wait until other player deals
                view = WaitForDealView(game_info, state_transition=self)
                self.window.show_view(view)

            elif card < opponent_card:
                game_info.is_dealer = True
                self.other_player.send_deal(game_info)

                add_to_crib_view = AddToCribView(game_info, state_transition= self)
                self.window.show_view(add_to_crib_view)

    def wait_deal_to_add_crib(self, game_info: GameInfo):
        from GameStates.WaitCribView import WaitCribView

        add_to_crib_view = WaitCribView(game_info, state_transition=self)
        self.window.show_view(add_to_crib_view)


    #       Cribbage to Cut transitions
    #========================================#

    """
    We take turns adding to the cribbage in order not to
    listen to ourselves when updating the database.
    
    Dealer will always add first, then wait
    NonDealer will wait first then add
    
    After, both will go to cut_deck
    """
    def wait_crib_transition(self, game_info: GameInfo, cards):
        from GameStates.CutDeckView import CutDeckView
        from GameStates.AddToCribView import AddToCribView
        from GameStates.WaitViews.WaitCutDeck import WaitCutDeck

        Backend.add_to_crib(game_info, cards)
        Backend.remove_from_other_hand(game_info, cards)

        # We picked a card, waited, next cut deck
        if game_info.is_dealer:
            # Should actually go to wait cut
            view = WaitCutDeck(game_info, state_transition=self)
            self.window.show_view(view)


        # waiting for other pick, we have not picked yet
        else:
            view = AddToCribView(game_info, state_transition=self)
            self.window.show_view(view)

    def pick_crib_transition(self, game_info: GameInfo, cards):
        from GameStates.WaitCribView import WaitCribView
        from GameStates.CutDeckView import CutDeckView

        Backend.add_to_crib(game_info, cards)
        Backend.remove_from_our_hand(game_info, cards)

        # We picked a card now we wait
        if game_info.is_dealer:
            view = WaitCribView(game_info, state_transition= self)
            self.window.show_view(view)

        # We already waited, now we picked, next we transition
        else:
            view = CutDeckView(game_info, state_transition= self)
            self.window.show_view(view)


    def add_crib_to_cut_deck(self, game_info: GameInfo, cards):
        from GameStates.CutDeckView import CutDeckView
        # Backend logic goes here if any

        Backend.add_to_crib(game_info, cards)


        # opponent_cards = Firebase.get_crib_picks()
        opponent_cards = self.other_player.add_to_cribbage(game_info)




        if game_info.is_dealer:
            cut_deck_view = CutDeckView(game_info, state_transition= self)
            self.window.show_view(cut_deck_view)
        else:
            #wait_view = WaitCutDeckView(game_info, state_transition= self)
            #self.window.show_view(wait_view)
            self.wait_for_cut_deck(game_info)


    def cut_deck_to_play(self, game_info, card):
        from GameStates.PlayView import PlayView
        #from GameStates.WaitView import WaitView

        game_info = Backend.cut_deck(game_info, card)
        
        self.other_player.send_cut(game_info)

        
        #wait_view = WaitView(game_info, state_transition= self)
        #self.window.show_view(wait_view)
        # Delete later, temporary solution
        self.wait_to_play(game_info)

    def wait_cut_to_wait_play(self, game_info: GameInfo, card):
        from GameStates.WaitViews.WaitPlay import WaitPlayView
        #TODO write logic
        game_info.top_card = card

        view = WaitPlayView( game_info= game_info, state_transition= self)
        self.window.show_view(view)
            
            
    def wait_for_cut_deck(self, game_info):
        from GameStates.PlayView import PlayView

        card = self.other_player.cut_deck(game_info)
        game_info = Backend.cut_deck(game_info, card)
        play_view = PlayView(game_info, state_transition= self)
        self.window.show_view(play_view)


    def play_to_wait(self, game_info: GameInfo, card: Card):
        from GameStates.PlayView import PlayView
        from GameStates.WaitViews.WaitPlay import WaitPlayView

        game_info.cards_in_play.append(card)
        game_info.our_hand.remove(card)

        play_score = Backend.play_card(game_info, card)
        game_info.our_score += play_score
        game_info.is_turn = False

        if game_info.cards_in_play == MAX_PLAYABLE_CARDS:
            #To show score button ?
            pass
        else:
            view = WaitPlayView(game_info, state_transition= self)
        self.window.show_view(view)
            


    def wait_to_play(self, game_info: GameInfo, card: Card):
        from GameStates.PlayView import PlayView

        game_info.cards_in_play.append(card)
        game_info.other_hand.remove(card)

        play_score = Backend.play_card(game_info, card)
        game_info.other_score += play_score
        game_info.is_turn = True

        play_view = PlayView(game_info, state_transition= self)
        self.window.show_view(play_view)

        if game_info.cards_in_play == MAX_PLAYABLE_CARDS:
            #To show score button ?
            view = None # For now
            pass
        else:
            view = PlayView(game_info, state_transition= self)
        self.window.show_view(view)





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


