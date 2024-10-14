
"""
 Idea of this class is that it will take over the logic of representing hand cards
 Should be called from Window
"""
from GUI.CardSprite import CardSprite


class PlayerHandDrawer:
    def __init__(self):
        self.player_hand_sprites = []

    def addSprite(self, sprite_pos_x, sprite_pos_y):
        sprite = CardSprite( position = [sprite_pos_x, sprite_pos_y] )
        self.player_hand_sprites.append( sprite )

    def draw(self):
        for sprite in self.player_hand_sprites:
            sprite.draw()
