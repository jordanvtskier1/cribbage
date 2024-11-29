class AnimationStep:
    def __init__(self, duration, behavior):
        self.duration = duration
        self.behavior = behavior
        self.completed = False

    def play(self):
        if self.duration <= 0:
            self.completed = True
            return
        else:
            self.duration = self.duration - 1
            is_done = self.behavior()
            if is_done:
                self.completed = True

