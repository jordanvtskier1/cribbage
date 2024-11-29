

class Animation:

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 650
    CENTER_CARD_LOCATION = [(SCREEN_WIDTH // 4) + 50, SCREEN_HEIGHT / 2]
    DECK_LOCATION = [50, SCREEN_HEIGHT / 2]

    def __init__(self):
        self.completed = True
        self.ready = False
        pass

    def play(self):
        pass

    def start(self):
        self.completed = False
        self.ready = True