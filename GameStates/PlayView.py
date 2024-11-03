import arcade

from GameStates.GameInfo import GameInfo
from GameStates.GameView import GameView


class PlayView(GameView):

    def __init__(self, game_info: GameInfo):
        super().__init__(game_info)


    def on_draw(self):
        self.clear()
        self.draw_scoreboard()
        self.draw_pegs()
        self.draw_score()
        self.draw_our_hand()
        self.draw_other_hand()

    # We assume it is always our turn
    def on_mouse_press(self, x, y, button, modifiers):
        clickable_sprites = arcade.SpriteList()
        for card in self.game_info.our_hand:
            clickable_sprites.append(card.sprite)
        cards_pressed = arcade.get_sprites_at_point((x, y), clickable_sprites)
        if len(cards_pressed) > 0:
            card = self.game_info.our_hand[self.game_info.our_hand.index(cards_pressed[-1])]
            self.transition.play_to_wait(game_info = self.game_info, card_sprite = card)