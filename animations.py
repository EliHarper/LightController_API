import time

from random import seed, randint
from light import convert_to_rgb, Color

# Scenes:
def paint_with_colors(strip, colors):
    # Accept color as hex
    print('Setting solid color to: {}'.format(colors))

    if type(colors[0]) == str:
        # Extracting ints from RgbColor object, which stores them as strings:
        rgb_tuples = convert_to_rgb(colors)
    else:
        rgb_tuples = colors
    print('RGBs: {}'.format(rgb_tuples))
    range_per_color = strip.numPixels() / len(rgb_tuples)
    range_per_color = int(range_per_color)
    rgb_tuple_index = 0

    for i in range(strip.numPixels()):
        # Make the strip show even(ish) amounts of each color, with remainder applied to last color
        if i % range_per_color == 0 and rgb_tuple_index < len(rgb_tuples):
            red, green, blue = rgb_tuples[rgb_tuple_index]
            rgb_tuple_index += 1
            # No idea why, but this function accepts in format GRB..
            strip.setPixelColor(i, Color(green, red, blue))
            strip.show()


def fire_projectiles(strip, colors, projectile_size=8):
    global stop_animation
    rgb_tuples = convert_to_rgb(colors)

    while not stop_animation:
        for tuple in rgb_tuples:
            if stop_animation:
                break
            red, green, blue = tuple
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(green, red, blue))
                strip.show()
                # i => head of projectile
                if i > (projectile_size - 1):
                    strip.setPixelColor(i - projectile_size, Color(0,0,0))


def breathe(strip, colors):
    global stop_animation
    paint_with_colors(strip, colors)

    while not stop_animation:
        # Increase brightness from 155 -> 255 (breathe upswing)
        for i in range(1, 128):
            strip.setBrightness(int(i))
            strip.show()
            time.sleep(1/1000)
        # Decrease brightness from 254 -> 156 (breathe downswing)
        for i in range(1, 127):
            strip.setBrightness(int(128-i))
            strip.show()
            time.sleep(1/1000)


def twinkle(strip, colors, pct_lit=.3):
    seed(14)

    tupleys = convert_to_rgb(colors)
    pixel_list = list(range(0, strip.numPixels()))
    indices_and_tupleys = dict({})

    for i in range(int(strip.numPixels() * pct_lit)):
        pixel_list_index = randint(0, len(pixel_list) - 1)
        scaled_light_index = pixel_list.pop(pixel_list_index)
        random_color_index = randint(0, len(tupleys) - 1)
        indices_and_tupleys.update({scaled_light_index : tupleys[random_color_index]})

    for pixel, color in indices_and_tupleys.items():
        red, green, blue = color
        strip.setPixelColor(pixel, Color(green, red, blue))
        strip.show()

    while not stop_animation:
        for _ in indices_and_tupleys.keys():
            off_index_of_dict = randint(0, len(indices_and_tupleys.keys()) - 1)
            off_index = list(indices_and_tupleys.keys())[off_index_of_dict]
            on_index = randint(0, len(pixel_list) - 1)
            on_color_index = randint(0, len(tupleys) - 1)
            red, green, blue = tupleys[on_color_index]

            strip.setPixelColor(off_index, Color(0, 0, 0))
            strip.show()
            pixel_list.append(off_index)

            strip.setPixelColor(on_index, Color(green, red, blue))
            strip.show()
            pixel_list.pop(on_index)


def bridge_fade(old, new, delta, idx, numSteps, step):
    """ Because sometimes you just want to make a truly horrific method signature. """
    # Figure if we're adding or subtracting at the color index (idx -> R, G, or B). New is the 
    #   transition's target; old is what we're transitioning from. 
    amountToChange = (delta // numSteps) * step
    if new[idx] > old[idx]:
        return old[idx] + amountToChange
    else:
        return old[idx] - amountToChange


def calculate_intermediates(colors, seconds=10):
    intermediate_colors = []
    rgb_colors = convert_to_rgb(colors)
    for i, color in enumerate(rgb_colors):
        # Wrap around to first item when on last index so it goes full-circle smoothly:
        next = (i + 1) % (len(rgb_colors))
        print('next: {}'.format(next))
        nextColor = rgb_colors[next]

        # Calculate the difference in green, red, and blue:
        diffR = abs(color[0] - nextColor[0])
        diffG = abs(color[1] - nextColor[1])
        diffB = abs(color[2] - nextColor[2])

        # Each "step" will be .5 seconds long; make a Color for each step and put in the array:
        numSteps = seconds * 2
        for currentStep in range(numSteps):
            # '//' -> Integer division to get floor; * currentStep to get progress toward next color per half sec:
            newR = bridge_fade(color, nextColor, diffR, 0, numSteps, currentStep)
            newG = bridge_fade(color, nextColor, diffG, 1, numSteps, currentStep)
            newB = bridge_fade(color, nextColor, diffB, 2, numSteps, currentStep)
            intermediate_colors.append(Color(newG, newR, newB))

    return intermediate_colors


def fade_between(strip, colors):
    # Figure a percent to change between colors, then populate an array with
    #   each intermediate color for the length of the full cycle:
    speed = 15
    intermediate_colors = calculate_intermediates(colors)
    print('fade_between')

    while not stop_animation:
        for color in intermediate_colors:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(1/speed)

