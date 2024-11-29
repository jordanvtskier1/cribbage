from Animations.AnimatedObject import AnimatedObject
from Animations.Animation import Animation
from Animations.AnimationStep import AnimationStep

SAD_BEE_SOURCE =  "./Sprites/sad_bee.png"

class PassAnimation(Animation):
    def __init__(self):
        super().__init__()


        self.sad_bee = AnimatedObject(source = SAD_BEE_SOURCE, scale = 0.25)
        self.sad_bee.set_position( [500, 500])
        self.animation_steps = [
            AnimationStep(
                duration = 90,
                behavior = self.shake_bee
            )
        ]

    def play(self):
        if self.completed or not self.ready:
            return

        for animation_step in self.animation_steps:
            if not animation_step.completed:
                animation_step.play()
                return
        self.completed = True

    def shake_bee(self):
        self.sad_bee.wiggle()
        self.sad_bee.draw()
        return False
