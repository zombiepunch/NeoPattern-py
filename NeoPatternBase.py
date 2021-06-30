import neopixel
import time
import abc
from abc import ABC, abstractmethod, abstractproperty

PIXEL_OFF = (0, 0, 0)
DEFAULT_BRIGHTNESS = 0.1

class Direction(object):
    FORWARD = 0
    REVERSE = 1


class NeoPatternBase(ABC):
    @property
    def num_pixels(self):
        """
        Number of pixels (read-only)
        """
        return len(self)

    @property
    def idx(self):
        """
        Index of current step in pattern
        """
        return self._index

    @idx.setter
    def idx(self, value):
        self._index = min(max(value, 0), self.num_pixels)

    @property
    def interval(self):
        """
        Pattern update interval in milliseconds
        """
        return self._interval

    @interval.setter
    def interval(self, value):
        """
        Set pattern update interval in milliseconds
        """
        self._interval = max(value, 0)

    @property
    def last_update(self):
        """
        Last update time in milliseconds
        """
        return self._last_update

    @property
    def color_1(self):
        """
        First color used in the pattern
        """
        return self._color_1

    @color_1.setter
    def color_1(self, value):
        """
        Set first color used in the pattern
        """
        if isinstance(value, int):
            value = (NeoPatternBase.red(value), 
                    NeoPatternBase.green(value), 
                    NeoPatternBase.blue(value))
            self._color_1 = value
        elif isinstance(value, tuple):
            self._color_1 = value

    @property
    def color_2(self):
        """
        Second color used in the pattern
        """
        return self._color_2

    @color_2.setter
    def color_2(self, value):
        """
        Set second color used in the pattern
        """
        if isinstance(value, int):
            value = (NeoPatternBase.red(value), 
                    NeoPatternBase.green(value), 
                    NeoPatternBase.blue(value))
            self._color_2 = value
        elif isinstance(value, tuple):
            self._color_2 = value

    @property 
    def direction(self):
        """
        Pattern direction from first pixel
        """
        return self._direction

    @property
    def total_steps(self):
        """
        Total number of steps in pattern
        """
        return self._total_steps

    @total_steps.setter
    def total_steps(self, value):
        """
        Set total number of steps in pattern
        """
        self._total_steps = value

    @property
    def on_complete(self):
        """
        Delegate to run when pattern completes
        """
        return self._on_complete

    @on_complete.setter
    def on_complete(self, value):
        """
        Set delegate to run when pattern completes
        """
        self._on_complete = value


    # class constructor
    @abstractmethod
    def __init__(self, neopixel: neopixel, callback, brightness=DEFAULT_BRIGHTNESS):
        self._neopixel = neopixel
        self.set_brightness(brightness)
        self._on_complete = callback
        self.reset()


    def __len__(self):
        """
        Number of pixels
        """
        if self._neopixel is not None:
            return self._neopixel.n
        else:
            return 0


    def set_brightness(self, brightness):
        """
        Set brightness of neopixel element synchronously
        """
        if self._neopixel is not None:
            self._neopixel.brightness = brightness

    
    def _increment(self):
        """
        Progresses to next step in pattern
        """
        if self._direction == Direction.FORWARD:
            self._index += 1
            if self._index >= self._total_steps:
                self._index = 0
                self._on_complete()
        else:
            self._index -= 1
            if self._index <= 0:
                self._index = (self._total_steps - 1)
                self._on_complete()


    def update(self):
        """
        Increments pattern and displays changes
        """
        self._update_pattern()
        self._neopixel.show()
        self._increment()


    @abstractmethod
    def _update_pattern(self):
        pass


    def reset(self):
        """
        Reset pattern to initial state
        """
        self.clear()
        self._last_update = NeoPatternBase._millis()
        self._interval = 0
        self._current_time = 0
        #self._color_1 = 0
        #self._color_2 = 0
        self._total_steps = 0
        self._index = 0
        self.set_brightness(DEFAULT_BRIGHTNESS)
        self._direction = Direction.FORWARD


    def reverse(self):
        """
        Reverse direction of the pattern
        """
        if self._direction == Direction.FORWARD:
            self._direction = Direction.REVERSE
            self._index = self._total_steps - 1
        else:
            self._direction = Direction.FORWARD
            self._index = 0


    def color_set(self, color: tuple[int, int, int]):
        """
        Set all pixels to a color (synchronously)
        """
        for i in range(self._neopixel.n):
            self._neopixel[i] = color
        
        self._neopixel.show()


    def clear(self):
        """
        Turn all pixels off
        """
        self.color_set(PIXEL_OFF)


    def has_white(self) -> bool:
        """
        Returns true if NeoPixel was initialized with RGBW
        """
        return True if self._neopixel.bpp == 4 and "W" in self._neopixel.byteorder else False


    @classmethod
    def _millis(cls) -> float:
        """
        Current time in milliseconds
        """
        return time.monotonic() * 1000


    @staticmethod
    def red(color):
        """
        Returns the Red component of a 32-bit color
        """
        if isinstance(color, tuple):
            return color[0]
        elif isinstance(color, int):
            return (color >> 16) & 0xFF
        else:
            return 0


    @staticmethod
    def green(color):
        """
        Returns the Green component of a 32-bit color
        """
        if isinstance(color, tuple):
            return color[1]
        elif isinstance(color, int):
            return (color >> 8) & 0xFF
        else:
            return 0


    @staticmethod
    def blue(color):
        """
        Returns the Blue component of a 32-bit color
        """
        if isinstance(color, tuple):
            return color[2]
        elif isinstance(color, int):
            return (color & 0xFF)
        else:
            return 0


    @staticmethod
    def white(color):
        """
        Returns the White component of a 32-bit color
        """
        if isinstance(color, tuple):
            return color[3] if len(color) == 4 else 0
        elif isinstance(color, int):
            return (color >> 24) & 0xFF
        else:
            return 0


    @staticmethod
    def dim_color_75(color) -> tuple[int, int, int]:
        """
        Returns color dimmed by 75%
        """
        if isinstance(color, int):
            return ((NeoPatternBase.red(color) >> 1),
                    (NeoPatternBase.green(color) >> 1),
                    (NeoPatternBase.blue(color) >> 1))
        else:
            return ((color[0] >> 1),
                    (color[1] >> 1),
                    (color[2] >> 1))


    @staticmethod
    def dim_color(color, percent):
        """
        Returns color dimmed by indicated percentage (0-1)
        """
        percent = min(max(percent, 0.0), 1.0)

        if isinstance(color, int):
            red = int(NeoPatternBase.red(color) * percent)
            green = int(NeoPatternBase.green(color) * percent)
            blue = int(NeoPatternBase.blue(color) * percent)

            return (red << 16) | (green << 8) | (blue)
        elif isinstance(color, tuple):
            return (int(color[0] * percent),
                    int(color[1] * percent),
                    int(color[2] * percent))


    @staticmethod
    def wheel(position: int) -> tuple[int, int, int]:
        """
        Input a value 0 to 255 to get a color value.
        (The colors are a transition r - g - b - back to r)
        """
        position = 255 - position
        if position < 85:
            return (255 - position * 3, 0, position * 3)
        elif position < 170:
            position -= 85
            return (0, position * 3, 255 - position * 3)
        else:
            position -= 170
            return (position * 3, 255 - position * 3, 0)