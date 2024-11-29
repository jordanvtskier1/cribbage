from GameStates.GameInfo import GameInfo
from Backend.BackendFunctions import Backend
from Card import Card
from Adversary.CPU import CPU
from Adversary.Multiplayer import Multiplayer
import arcade

MAX_PLAYABLE_CARDS = 8


class StateTransitionBackend:
    def __init__(self, window: arcade.Window):
        self.window = window

    def cpu_to_pick_card(self, game_info: GameInfo):
        from GameStates.ActiveViews.PickCardView import PickCardView

        game_info.is_multiplayer = False

        game_info.other_player = CPU()
        game_info = Backend.create_deck(game_info)
        pick_card_view = PickCardView(game_info, state_transition=self)
        self.window.show_view(pick_card_view)

    def create_game_to_pick_card(self, game_info: GameInfo, game_name):
        from GameStates.ActiveViews.PickCardView import PickCardView

        game_info.other_player = Multiplayer()

        game_info = Backend.create_deck(game_info)
        game_info.opponent = "player2"
        game_info.player = "player1"
        game_info.other_player.create_game(game_info=game_info, game_name=game_name)
        pick_card_view = PickCardView(game_info, self)
        self.window.show_view(pick_card_view)

    def join_game_to_pick_card(self, game_info: GameInfo, game_name: str):
        from GameStates.ActiveViews.PickCardView import PickCardView
        from GameStates.MenuViews.JoinInputView import JoinInputView

        game_info.other_player = Multiplayer()
        game_info.opponent = "player1"
        game_info.player = "player2"
        game_info.other_player.join_game(game_info=game_info, game_name=game_name)

        # If no deck, then game does not exist. Return to Join view
        if not game_info.deck:
            join_game_view = JoinInputView(game_info=game_info, state_transition=self)
            self.window.show_view(join_game_view)

        else:
            pick_card_view = PickCardView(game_info, state_transition=self)
            self.window.show_view(pick_card_view)

    def pick_card_to_deal(self, game_info: GameInfo, card: Card, opponent_card: Card):

        from GameStates.ActiveViews.PickCardView import PickCardView
        from GameStates.WaitViews.WaitForDealView import WaitForDealView
        from GameStates.ActiveViews.AddToCribView import AddToCribView

        # means that both players picked same card, return to pick card view
        if card.getRankAsInt() == opponent_card.getRankAsInt():
            view = PickCardView(game_info, state_transition=self)
            view.is_showing_again()
            self.window.show_view(view)

        else:
            if card.getRankAsInt() > opponent_card.getRankAsInt():
                game_info.is_dealer = False

            elif card.getRankAsInt() < opponent_card.getRankAsInt():
                game_info.is_dealer = True
                game_info = Backend.deal_cards(game_info)
                game_info.other_player.send_deal(game_info)

            view = WaitForDealView(game_info, state_transition=self)
            self.window.show_view(view)

    def wait_deal_to_add_crib(self, game_info: GameInfo):
        from GameStates.WaitViews.WaitCribView import WaitCribView
        from GameStates.ActiveViews.AddToCribView import AddToCribView

        if game_info.is_dealer:
            next_view = AddToCribView(game_info, state_transition=self)
        else:
            next_view = WaitCribView(game_info, state_transition=self)
        self.window.show_view(next_view)

    #       Cribbage to Cut transitions
    # ========================================#

    """
    We take turns adding to the cribbage in order not to
    listen to ourselves when updating the database.

    Dealer will always add first, then wait
    NonDealer will wait first then add

    After, both will go to cut_deck
    """

    def wait_crib_transition(self, game_info: GameInfo, cards):
        from GameStates.ActiveViews.AddToCribView import AddToCribView
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
        from GameStates.WaitViews.WaitCribView import WaitCribView
        from GameStates.ActiveViews.CutDeckView import CutDeckView

        Backend.add_to_crib(game_info, cards)
        Backend.remove_from_our_hand(game_info, cards)

        # We picked a card now we wait
        if game_info.is_dealer:
            view = WaitCribView(game_info, state_transition=self)
            self.window.show_view(view)

        # We already waited, now we picked, next we transition
        else:
            view = CutDeckView(game_info, state_transition=self)
            self.window.show_view(view)

    def add_crib_to_cut_deck(self, game_info: GameInfo, cards):
        from GameStates.ActiveViews.CutDeckView import CutDeckView
        # Backend logic goes here if any

        Backend.add_to_crib(game_info, cards)

        # opponent_cards = Firebase.get_crib_picks()
        opponent_cards = self.other_player.add_to_cribbage(game_info)

        if game_info.is_dealer:
            cut_deck_view = CutDeckView(game_info, state_transition=self)
            self.window.show_view(cut_deck_view)
        else:
            # wait_view = WaitCutDeckView(game_info, state_transition= self)
            # self.window.show_view(wait_view)
            self.wait_for_cut_deck(game_info)

    def cut_deck_to_play(self, game_info, card):
        # from GameStates.WaitView import WaitView

        game_info = Backend.cut_deck(game_info, card)

        self.other_player.send_cut(game_info)

        # wait_view = WaitView(game_info, state_transition= self)
        # self.window.show_view(wait_view)
        # Delete later, temporary solution
        self.wait_to_play(game_info)

    def wait_cut_to_wait_play(self, game_info: GameInfo, card):
        from GameStates.WaitViews.WaitPlay import WaitPlayView
        from GameStates.ActiveViews.PlayView import PlayView

        game_info = Backend.cut_deck(game_info, card)

        game_info.our_hand_score = Backend.calculate_hand_score(game_info=game_info, hand=game_info.our_hand)
        game_info.other_hand_score = Backend.calculate_hand_score(game_info=game_info, hand=game_info.other_hand)

        if game_info.is_dealer:
            # TODO: add point if cut card was a jack
            view = WaitPlayView(game_info=game_info, state_transition=self)
            self.window.show_view(view)
        else:
            view = PlayView(game_info=game_info, state_transition=self)
            self.window.show_view(view)

    def wait_for_cut_deck(self, game_info):
        from GameStates.ActiveViews.PlayView import PlayView

        card = self.other_player.cut_deck(game_info)
        game_info = Backend.cut_deck(game_info, card)
        play_view = PlayView(game_info, state_transition=self)
        self.window.show_view(play_view)

    def play_to_wait(self, game_info: GameInfo, card: Card):
        from GameStates.WaitViews.WaitPlay import WaitPlayView
        from GameStates.MenuViews.EndGameView import EndGameView
        if not card.is_empty_card():
            play_score = Backend.play_card(game_info, card)
            game_info.cards_in_play.append(card)
            game_info.our_hand.remove(card)
            game_info.our_score += play_score

            play_total = Backend.get_in_play_count(game_info)

            # If play hits 31
            if play_total == game_info.MAX_TOTAL:
                game_info.other_score += 1

        if not Backend.can_someone_play(game_info):
            Backend.start_new_in_play_count(game_info)

        #  game_info.other_player.send_play(game_info, card)
        game_is_over = Backend.check_game_over(game_info)
        if game_is_over:
            view = EndGameView(game_info, state_transition=self)
            self.window.show_view(view)
        else:
            wait_play_view = WaitPlayView(game_info, state_transition=self)
            self.window.show_view(wait_play_view)

    def wait_to_play(self, game_info: GameInfo, card: Card):
        from GameStates.WaitViews.WaitPlay import WaitPlayView
        from GameStates.MenuViews.EndGameView import EndGameView
        from GameStates.ActiveViews.PlayView import PlayView

        if not card.is_empty_card():
            play_score = Backend.play_card(game_info, card)
            game_info.cards_in_play.append(card)
            # for c in game_info.other_hand:
            #     if c.suit == card.suit and c.rank == card.rank:
            #         game_info.other_hand.remove(c)
            #         break
            game_info.other_hand.remove(card)
            game_info.other_score += play_score
            play_total = Backend.get_in_play_count(game_info)

            # If opponent play hits 31 add a point
            if play_total == game_info.MAX_TOTAL:
                game_info.other_score += 1

        # TODO add a plus score to whoever plays the last card
        if not Backend.can_someone_play(game_info):
            Backend.start_new_in_play_count(game_info)

        game_is_over = Backend.check_game_over(game_info)
        if game_is_over:
            view = EndGameView(game_info, state_transition=self)
            self.window.show_view(view)
        else:
            view = PlayView(game_info, state_transition= self)
            self.window.show_view(view)

        # Where should this go ?
        # # No cards we can play
        # if not playable_cards:
        #     #TODO: add logic if they have no cards
        #     if len(game_info.other_hand) == 0:
        #         if len(game_info.our_hand) == 0:
        #             self.play_to_show_score(game_info=game_info)
        #         else:
        #             game_info.other_score += 1
                        # WE DONT WANT TO RESTART LIKE THIS
        #               game_info.cards_in_play = []
        #               game_info.current_count = 0



    def opponent_cannot_play(self, game_info: GameInfo):
        from GameStates.WaitViews.WaitPlay import WaitPlayView
        from GameStates.ActiveViews.PlayView import PlayView

        game_info.our_score += 1

        play_total = sum(card.getValue() for card in game_info.cards_in_play)
        playable_cards = [
            card for card in game_info.our_hand
            if play_total + card.getValue() <= game_info.MAX_TOTAL
        ]

        # cannot play any cards
        if not playable_cards:
            if len(game_info.other_hand) >= 1:
                game_info.cards_in_play = []
                game_info.current_count = 0
                wait_play_view = WaitPlayView(game_info, state_transition=self)
                self.window.show_view(wait_play_view)
            elif len(game_info.our_hand) == 0:
                self.play_to_show_score(game_info=game_info)
        else:
            view = PlayView(game_info, state_transition=self)
            self.window.show_view(view)

    def play_to_show_score(self, game_info: GameInfo):
        from GameStates.ActiveViews.ShowScoreView import ShowScoreView
        # Get hand scores from before play
        game_info.our_score += game_info.our_hand_score
        game_info.other_score += game_info.other_hand_score

        crib_score = Backend.calculate_crib_score(game_info)
        if game_info.is_dealer:
            game_info.our_score += crib_score
        else:
            game_info.other_score += crib_score

        game_info.crib_score = crib_score

        # opponent_score = Firebase.getOppScore()
        # game_info.other_score = opponent_score
        self.window.show_view(ShowScoreView(game_info, state_transition=self))

    def show_score_to_crib(self, game_info: GameInfo):
        from GameStates.ActiveViews.AddToCribView import AddToCribView
        from GameStates.WaitViews.WaitForDealView import WaitForDealView
        from GameStates.MenuViews.EndGameView import EndGameView

        Backend.set_up_next_round(game_info=game_info)
        game_info.other_player.send_deal(game_info)

        game_is_over = Backend.check_game_over(game_info)
        if game_is_over:
            view = EndGameView(game_info, state_transition=self)
            self.window.show_view(view)
        else:
            next_view = WaitForDealView(game_info, state_transition=self)
            self.window.show_view(next_view)


