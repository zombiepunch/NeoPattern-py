import neopixel

from NeoPatternBase import Direction, NeoPatternBase, PIXEL_OFF

class ColorWipePattern(NeoPatternBase):
    # class constructor
    def __init__(self, 
                 neopixel: neopixel, 
                 interval, 
                 callback, 
                 color_1, 
                 color_2=PIXEL_OFF, 
                 direction=Direction.FORWARD, 
                 brightness=0.1):
        super().__init__(neopixel, callback, brightness)
        self.interval = interval
        self.color_1 = color_1
        self.color_2 = color_2
        
        if direction != self.direction:
            self.reverse()


    def _update_pattern(self):
        if self.idx >= self.num_pixels:
            self[self.idx % self.num_pixels] = self.color_2
        else:
            self[self.idx] = self.color_1