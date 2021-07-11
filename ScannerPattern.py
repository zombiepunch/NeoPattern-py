import neopixel
from NeoPatternBase import DEFAULT_BRIGHTNESS, Direction, NeoPatternBase, Colors

class ScannerPattern(NeoPatternBase):
    # class constructor
    def __init__(self,
                 neopixel: neopixel,
                 interval,
                 callback,
                 color_1,
                 color_2=Colors.OFF,
                 direction=Direction.FORWARD,
                 brightness=DEFAULT_BRIGHTNESS):
        super().__init__(neopixel, callback, brightness, direction)
        self.interval = interval
        self.total_steps = (self.num_pixels - 1) * 2
        self.color_1 = color_1
        self.color_2 = color_2
        self.idx = 0 if direction == Direction.FORWARD else self.total_steps - 1


    def _update_pattern(self):
        for i in range(self.num_pixels):
            if i == self.idx:
                self[i] = self.color_1
            elif i == (self.total_steps - self.idx):
                self[i] = self.color_1
            else:
                self[i] = self.dim_color_75(self[i])