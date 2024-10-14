import arcade

# Constants
SCALING = 1
SOURCE = "./Sprites/Cards/WormSuits/K_Worm.png"

class CardSprite:

    """
    Given a Card ( number and suit ) we should match it to its sprite ( file location )
    and also paint it
    """
    def __init__(self, position):
        self.sprite = arcade.Sprite( SOURCE, SCALING)
        self.sprite.center_x = position[0]
        self.sprite.center_y = position[1]
        pass

    def draw(self):
        self.sprite.draw()