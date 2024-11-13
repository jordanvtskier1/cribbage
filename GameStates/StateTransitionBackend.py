from Adversary.OtherPlayerLogic import OtherPlayerLogic
from GameStates.GameInfo import GameInfo
from Backend.BackendFunctions import Backend
from Card import Card


class StateTransitionBackend:
    def __init__(self, window):
        self.window = window

        #Uninitialized other player
        self.other_player = OtherPlayerLogic()


    def set_other_player(self, other_player_logic):
        self.other_player = other_player_logic

    def menu_to_pick_card(self, game_info: GameInfo):
        from GameStates.PickCardView import PickCardView

        game_info = Backend.create_deck(game_info)
        
        pick_card_view = PickCardView(game_info, state_transition= self)
        self.window.show_view(pick_card_view)


    def pick_card_to_add_crib(self, game_info: GameInfo, card):
        from GameStates.AddToCribView import AddToCribView
        from GameStates.PickCardView import PickCardView

        opponent_card = self.other_player.pick_card(game_info)
        if card> opponent_card:
            game_info.is_dealer = False
            game_info.has_crib = False
            game_info.is_turn = True
        # This will look weird if we add it right now,  but its how we should play
        # elif card == opponent_card:
        #     Backend.create_deck(game_info)
        #     self.window.show_view(
        #         PickCardView(game_info, state_transition= self)
        #     )
        else:
            game_info.is_dealer = True
            game_info.has_crib = True
            game_info.is_turn = False

        game_info = Backend.deal_cards(game_info)

        add_to_crib_view = AddToCribView(game_info, state_transition= self)
        self.window.show_view(add_to_crib_view)

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


