import random
from PIL import Image
from numpy import ones, zeros, uint8

# create segment
def createSegment():
    rgba = zeros((50, 150, 4), dtype=uint8)
    rgba[:, :, 3] = ones((50, 150), dtype=uint8) * 255 # alpha is last channel
    rgba[:, :, 1] = ones((50, 150), dtype=uint8) * 255 # channel 0 is red, 1 is green, 2 is blue

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

    return Image.fromarray(rgba, mode='RGBA')

# one horizontal segment is 150 pixels wide by 50 pixels tall with transparent background
segmentHorizontal = createSegment() #Image.open('seg.png')
segmentVertical = segmentHorizontal.copy().rotate(90, expand=True)

# doing a gap of 5 pixels between things
# Overall height = 5 + 30 + 150 + 10 + 150 + 30 + 5= 380
# Overall width = 5 + 30 + 150 + 30 + 5 = 220
def emulate7SegDisplay(digit):
    sevenSegDisplay = Image.new('RGBA', (220, 380))
    if digit & (1 << 0):
        sevenSegDisplay.alpha_composite(segmentHorizontal, (35, 5))    # top
    if digit & (1 << 1):
        sevenSegDisplay.alpha_composite(segmentVertical,   (165, 35))  # top right side
    if digit & (1 << 2):
        sevenSegDisplay.alpha_composite(segmentVertical,   (165, 195)) # bottom right side
    if digit & (1 << 3):
        sevenSegDisplay.alpha_composite(segmentHorizontal, (35, 325))  # bottom
    if digit & (1 << 4):
        sevenSegDisplay.alpha_composite(segmentVertical,   (5, 195))   # bottom left side
    if digit & (1 << 5):
        sevenSegDisplay.alpha_composite(segmentVertical,   (5, 35))    # top left side
    if digit & (1 << 6):
        sevenSegDisplay.alpha_composite(segmentHorizontal, (35, 165))  # middle
    return sevenSegDisplay


displays = []
for digit in digits:
    displays.append(emulate7SegDisplay(digit))

displays[0].save('output.gif', save_all=True, append_images=displays[1:], optimize=True, loop=0, duration=2000)
