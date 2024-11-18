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




class StateTransitionBackend:
    def __init__(self, window: arcade.Window):
        self.window = window
        #self.database_ref = init()
        


    def create_game_to_pick_card(self, game_info: GameInfo, game_name):
        from GameStates.PickCardView import PickCardView

        self.other_player = Multiplayer()
        self.other_player.create_game(game_info=game_info, game_name=game_name)
        pick_card_view = PickCardView(game_info, self)
        self.window.show_view(pick_card_view)


    
    def join_game_to_pick_card(self, game_info: GameInfo, game_name: str): 
        from GameStates.PickCardView import PickCardView
        from GameStates.MenuViews.JoinInputView import JoinInputView
        

        self.other_player = Multiplayer()
        self.other_player.join_game(game_info=game_info, game_name=game_name)

        if not game_info.deck:
             join_game_view = JoinInputView(game_info=game_info, state_transition=self)
             self.window.show_view(join_game_view)

        else:
            pick_card_view = PickCardView(game_info, state_transition=self)
            self.window.show_view(pick_card_view)
        



    def pick_card_to_add_crib(self, game_info: GameInfo, card: Card):
        from GameStates.AddToCribView import AddToCribView
        from GameStates.PickCardView import PickCardView
        
        opponent_card = self.other_player.pick_card(game_info=game_info, card=card)

        # means that both players picked same card, return to pick card view
        if card == opponent_card:
            view = PickCardView(game_info, state_transition=self)
            self.window.show_view(view)
        else:
            if card > opponent_card:
                game_info.is_dealer = False
                self.other_player.get_deal(game_info)

            elif card < opponent_card:
                game_info.is_dealer = True
                self.other_player.send_deal(game_info)

            add_to_crib_view = AddToCribView(game_info, state_transition= self)
            self.window.show_view(add_to_crib_view)


        

    def add_crib_to_cut_deck(self, game_info: GameInfo, card1, card2):
        from GameStates.CutDeckView import CutDeckView
        # Backend logic goes here if any

        Backend.add_to_crib(game_info, [card1, card2])
        Backend.remove_from_our_hand(game_info, [card1, card2])

        # opponent_cards = Firebase.get_crib_picks()
        opponent_cards = self.other_player.add_to_cribbage(game_info)

        Backend.add_to_crib(game_info, [opponent_cards[0], opponent_cards[1]])
        Backend.remove_from_other_hand(game_info, [opponent_cards[0],  opponent_cards[1]])


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
            
            
    def wait_for_cut_deck(self, game_info):
        from GameStates.PlayView import PlayView

        card = self.other_player.cut_deck(game_info)
        game_info = Backend.cut_deck(game_info, card)
        play_view = PlayView(game_info, state_transition= self)
        self.window.show_view(play_view)


    def play_to_wait(self, game_info: GameInfo, card: Card):
        from GameStates.PlayView import PlayView
        #from GameStates.WaitView import WaitView

        played_card_sum = sum(card.getValue() for card in game_info.cards_in_play)

        if played_card_sum + card.getValue() > 31:
            game_info.can_play = False

            self.other_player.send_play(game_info, None)
            #TODO add output message
            

        else:
            game_info.cards_in_play.append(card)
            game_info.our_hand.remove(card)

            play_score = Backend.play_card(game_info, card)
            game_info.our_score += play_score
            game_info.is_turn = False

            self.other_player.send_play(game_info, card)

        # TODO: create WaitView
        #wait_view = WaitView(game_info, state_transition= self)
        #self.window.show_view(wait_view)
        self.wait_to_play(game_info)
            


    def wait_to_play(self, game_info: GameInfo):
        from GameStates.PlayView import PlayView

        other_card = self.other_player.play_card(game_info)
        #TODO add backend logic for playing cards ? I dont know how it works
        game_info.cards_in_play.append(other_card)
        game_info.other_hand.remove(other_card)
        game_info.is_turn = True

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


