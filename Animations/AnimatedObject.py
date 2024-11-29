import arcade
import math

DELTA_TIME = 1/60

class AnimatedObject:
    def __init__(self, source: str, scale: float):
        self.scale = scale
        self.sprite = arcade.Sprite(source, scale=scale)

        self.angle_offset = 0

    def set_position(self, position):
        self.sprite.set_position(position[0], position[1])

    def draw(self):
        self.sprite.draw()

    def change_sprite(self, source):
        self.sprite = arcade.Sprite(source)

    def wiggle(self):
        self.angle_offset += DELTA_TIME * 6
        self.sprite.angle = math.sin(self.angle_offset) * 15

