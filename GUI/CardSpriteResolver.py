class CardSpriteResolver:


    generic_path = "./Sprites/Cards"

    @classmethod
    def getSpriteFile(cls, suit, value):
        path_to_file = cls.generic_path + "/"+ str(suit)
        path_to_file += "/" + str(value) + ".png"
        return path_to_file

