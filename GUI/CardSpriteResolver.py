class CardSpriteResolver:

    generic_path = "./Sprites/Cards"
    def __init__(self):
        pass

    def getSpriteFile(self, suit, value):
        path_to_file = self.generic_path + "/"+ str(suit)
        path_to_file += "/" + str(value) + ".png"
        return path_to_file

