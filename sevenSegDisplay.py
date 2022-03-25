import random
from PIL import Image
from numpy import ones, zeros, uint8


class sevenSegDisplay:
    """
    Seven Segment Display Emulator.

    This class creates segments for a seven segment display and
    will light them up emulating a real seven segment display
    """
    # mapping showing how each hex character maps
    # to 7 bits going into the display
    mapping = {
        0x0: 0x3f,  0x1: 0x06,  0x2: 0x5b,  0x3: 0x4f,
        0x4: 0x66,  0x5: 0x6d,  0x6: 0x7d,  0x7: 0x07,
        0x8: 0x7f,  0x9: 0x6f,  0xA: 0x77,  0xB: 0x7c,
        0xC: 0x39,  0xD: 0x5e,  0xE: 0x79,  0xF: 0x71,
    }

    def __init__(self, color: str = 'green') -> 'sevenSegDisplay':
        """
        Create one of the segments for the display.

        One horizontal segment is 150 pixels wide by 50 pixels tall
        with transparent background
        """
        rgba = zeros((50, 150, 4), dtype=uint8)
        # alpha is last channel
        rgba[:, :, 3] = ones((50, 150), dtype=uint8) * 255

        if color == 'red':
            rgba[:, :, 0] = ones((50, 150), dtype=uint8) * 255
        elif color == 'green':
            rgba[:, :, 1] = ones((50, 150), dtype=uint8) * 255
        elif color == 'blue':
            rgba[:, :, 2] = ones((50, 150), dtype=uint8) * 255
        else:
            print('Color not supported, please use red, green, or blue')
            return

        # need to shape the alpha channel correctly to not overlap pixels
        for x in range(25):
            for y in range(25):
                if x + y < 25:
                    rgba[y, x, 3] = 0
                else:
                    rgba[y+25, x+125, 3] = 0

                if x > y:
                    rgba[y, x+125, 3] = 0
                else:
                    rgba[y+25, x, 3] = 0

        self.segmentHorizontal = Image.fromarray(rgba, mode='RGBA')
        self.segmentVertical = self.segmentHorizontal.rotate(90, expand=True)

    def display(self, digit: int) -> 'Image':
        """
        Creating an image of a 7 segment display given a digit to display.

        Doing a gap of 5 pixels between segments
        Overall height = 5 + 30 + 150 + 10 + 150 + 30 + 5 = 380
        Overall width = 5 + 30 + 150 + 30 + 5 = 220
        """
        picture = Image.new('RGBA', (220, 380))

        if digit & (1 << 0):  # top
            picture.alpha_composite(self.segmentHorizontal, (35, 5))
        if digit & (1 << 1):  # top right side
            picture.alpha_composite(self.segmentVertical,   (165, 35))
        if digit & (1 << 2):  # bottom right side
            picture.alpha_composite(self.segmentVertical,   (165, 195))
        if digit & (1 << 3):  # bottom
            picture.alpha_composite(self.segmentHorizontal, (35, 325))
        if digit & (1 << 4):  # bottom left side
            picture.alpha_composite(self.segmentVertical,   (5, 195))
        if digit & (1 << 5):  # top left side
            picture.alpha_composite(self.segmentVertical,   (5, 35))
        if digit & (1 << 6):  # middle
            picture.alpha_composite(self.segmentHorizontal, (35, 165))

        return picture
