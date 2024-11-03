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

#============================================================#
# Setters

    def setSuit(self, suit):
        self.suit = suit

    def setRank(self, rank):
        self.rank = rank

    def setSprite(self, source):
        self.sprite = arcade.Sprite(source, 0.5)

    def setPosition(self, position):
        self.sprite.center_x = position[0]
        self.sprite.center_y = position[1]

#============================================================#
# Getters

    def getSuit(self):
        return self.suit
    
    def getRank(self):
        return self.rank
    
    def getValue(self):
        if self.rank == "Ace":
            return 1
        elif self.rank in ["Jack", "Queen", "King"]:
            return 10
        else:
            return self.rank
        
    def getRankAsInt(self):
        if self.rank == "Ace":
            return 1
        elif self.rank == "Jack":
            return 11
        elif self.rank == "Queen":
            return 12
        elif self.rank == "King":
            return 13
        else:
            return self.rank
    
    def getSprite(self):
        return self.sprite

    def getPosition(self):
        return [self.sprite.center_x, self.sprite.center_y]
    
#============================================================#
# Drawing

    def draw(self):
        self.sprite.draw()
    
#============================================================#
# To String

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)
