import neopixel

from NeoPatternBase import Direction, NeoPatternBase, Colors

class ColorWipePattern(NeoPatternBase):
    # class constructor
    def __init__(self, 
                 neopixel: neopixel, 
                 interval, 
                 callback, 
                 color_1, 
                 color_2=Colors.OFF, 
                 direction=Direction.FORWARD, 
                 brightness=0.1):
        super().__init__(neopixel, callback, brightness, direction)
        self.interval = interval
        self.total_steps = self.num_pixels * 2
        self.idx = 0 if direction == Direction.FORWARD else self.num_pixels
        self.color_1 = color_1
        self.color_2 = color_2


    def _update_pattern(self):
        if self.direction == Direction.FORWARD:
            if self.idx >= self.num_pixels:
                self[self.idx % self.num_pixels] = self.color_2
            else:
                self[self.idx] = self.color_1
        else:
            if self.idx > self.num_pixels:
                self[(self.idx - 1) % self.num_pixels] = self.color_1
            else:
                self[(self.idx - 1)] = self.color_2