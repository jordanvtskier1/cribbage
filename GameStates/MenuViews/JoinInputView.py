from GameStates.MenuViews.GameKeyInputView import GameKeyInputView


class JoinInputView(GameKeyInputView):

    def __init__(self, game_info, state_transition):
        label = "Join Game Key"
        self.game_info = game_info
        self.state_transition = state_transition
        super().__init__(label=label,
                         to_next_view=self.to_next_view,
                         game_info=self.game_info,
                         state_transition=self.state_transition)

    def to_next_view(self, game_key):
        pass
