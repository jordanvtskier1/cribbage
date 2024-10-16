# A Card object to represent one of the 52 cards in a standard deck
# CS 3050: Software Engineering
#

import arcade

class Card:

#============================================================#
# Constructor

    def __init__(self, suit, rank, source="./Sprites/PlayingCards.png", position=[500, 500]):
        self.setSuit(suit)
        self.setRank(rank)
        # Not required by constructor so that back end can make all cards
        # Then front end can use setters to add sprites and locations
        self.setSprite(source)
        self.setPosition(position)

    def setSprite(self, source):
        self.sprite = arcade.Sprite(source, 0.05)

    def setPosition(self, position):
        self.sprite.center_x = position[0]
        self.sprite.center_y = position[1]

    def draw(self):
        self.sprite.draw()

#============================================================#
# Setters

    def setSuit(self, suit):
        self.suit = suit

    def setRank(self, rank):
        self.rank = rank

#============================================================#
# Getters

    def getSuit(self):
        return self.suit
    
    def getRank(self):
        return self.rank
    
#============================================================#
# To String

    def __str__(self):
        return str.format("{self.rank} of {self.suit}s")
