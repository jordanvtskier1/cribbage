# This class serves as a contract to specify what all "wait states" should be waiting for
import GameStates.GameInfo as GameInfo

class OtherPlayerLogic:
    def __init__(self):
        pass

    # Choosing a card in the pick card state
    def pick_card(self, game_info: GameInfo):
        pass

    def add_to_cribbage(self, game_info: GameInfo):
        pass

    def cut_deck(self, game_info: GameInfo):
        pass

    def play_card(self, game_info: GameInfo):
        pass