import neopixel
from NeoPatternBase import DEFAULT_BRIGHTNESS, Direction, NeoPatternBase, Colors

class RainbowCyclePattern(NeoPatternBase):
    # class constructor
    def __init__(self, 
                 neopixel: neopixel, 
                 interval, 
                 callback, 
                 direction=Direction.FORWARD, 
                 brightness=DEFAULT_BRIGHTNESS):
        super().__init__(neopixel, callback, brightness, direction)
        self.interval = interval
        self.total_steps = 255
        self.idx = 0 if direction == Direction.FORWARD else self.total_steps


    def _update_pattern(self):
        for i in range(self.num_pixels):
            self[i] = self.wheel(((i * 256 // self.num_pixels) + self.idx) & 255)