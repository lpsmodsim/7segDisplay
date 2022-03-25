import sevenSegDisplay

# supported colors
colors = ['red', 'green', 'blue']
# create a sevenSegDisplay for each color
displays = [sevenSegDisplay.sevenSegDisplay(color) for color in colors]

# mapping showing how each hex character maps to 7 bits going into the display
mapping = {
    0x0: 0x3f,  0x1: 0x06,  0x2: 0x5b,  0x3: 0x4f,
    0x4: 0x66,  0x5: 0x6d,  0x6: 0x7d,  0x7: 0x07,
    0x8: 0x7f,  0x9: 0x6f,  0xA: 0x77,  0xB: 0x7c,
    0xC: 0x39,  0xD: 0x5e,  0xE: 0x79,  0xF: 0x71,
}

# for each color display, we want to demonstrate what each digit looks like
output = []
for display in displays:
    for digit in mapping.values():
        output.append(display.display(digit))

# can save all the images as a gif if you want
output[0].save('output.gif', save_all=True,
               append_images=output[1:], optimize=True,
               loop=0, duration=1000)
