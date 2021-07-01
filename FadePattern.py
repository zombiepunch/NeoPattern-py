import neopixel
from NeoPatternBase import DEFAULT_BRIGHTNESS, Direction, NeoPatternBase, Colors

class FadePattern(NeoPatternBase):
    # class constructor
    def __init__(self, 
                 neopixel: neopixel, 
                 interval, 
                 steps,
                 callback, 
                 color_1, 
                 color_2=Colors.OFF, 
                 direction=Direction.FORWARD, 
                 brightness=DEFAULT_BRIGHTNESS):
        super().__init__(neopixel, callback, brightness, direction)
        self.interval = interval
        self.total_steps = steps
        self.idx = 0 if direction == Direction.FORWARD else self.total_steps
        self.color_1 = color_1
        self.color_2 = color_2


    def _update_pattern(self):
        steps = self.total_steps
        idx = self.idx

        red = ((self.color_1[0] * (steps - idx)) + (self.color_2[0] * idx)) / steps
        green = ((self.color_1[1] * (steps - idx)) + (self.color_2[1] * idx)) / steps
        blue = ((self.color_1[2] * (steps - idx)) + (self.color_2[2] * idx)) / steps

        self.color_set((red, green, blue))
        print("Color: " + str((red, green, blue)))