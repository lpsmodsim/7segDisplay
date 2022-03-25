import sevenSegDisplay as sevenSeg

# supported colors
colors = ['red', 'green', 'blue']
# create a sevenSegDisplay for each color
displays = [sevenSeg.sevenSegDisplay(color) for color in colors]

# for each color display, we want to demonstrate what each digit looks like
output = []
# we only need to loop through the values as that is
# what the display accepts
for digit in sevenSeg.sevenSegDisplay.mapping.values():
    for disp in displays:
        output.append(disp.display(digit))

# can save all the images as a gif if you want
output[0].save('output.gif', save_all=True,
               append_images=output[1:], optimize=True,
               loop=0, duration=300)
