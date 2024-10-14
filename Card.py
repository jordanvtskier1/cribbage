# A Card object to represent one of the 52 cards in a standard deck
# CS 3050: Software Engineering
#

class Card:

#============================================================#
# Constructor

    def __init__(self, suit, rank):
        self.setSuit(suit)
        self.setRank(rank)

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
