from GameStates.MenuViews.GameKeyInputView import GameKeyInputView
from GameStates.StateTransitionBackend import StateTransitionBackend
class HostInputView(GameKeyInputView):

    def __init__(self, game_info, state_transition: StateTransitionBackend):
        label = "Host Game Key"
        self.game_info = game_info
        self.state_transition = state_transition
        super().__init__(label = label,
                         to_next_view= self.to_next_view,
                         game_info= self.game_info,
                         state_transition= self.state_transition )

    def to_next_view (self, game_key):
        self.state_transition.create_game_to_pick_card(game_info=self.game_info, game_name=game_key)
