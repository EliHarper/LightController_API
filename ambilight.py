from operator import itemgetter
from PIL import ImageGrab, Image
import time
import gc


MIN_RANGE = 10
NUMBER_OF_COLORS = 5
RESIZE_DIMENSIONS = (150,150)
VERTICAL_COLUMNS = 15


class Ambilight:    
    def __init__(self):
        self._on = False

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, new):
        if type(new) == bool:
            self._on = new



def get_screenshot():
    return ImageGrab.grab()


def get_max_color_freq_idx(colors: list) -> int:
    max_color_index = colors.index(max(colors, key = itemgetter(0)))
    
    return max_color_index


def get_top_x_colors(colors: list, x: int):
    top_colors = []

    for iteration in range(x):
        max_color_index = get_max_color_freq_idx(colors)
        color_and_freq = colors[max_color_index]        
        # Just get the rgb tuple, not the tuple and its frequency:
        rgb = color_and_freq[1]
        
        # Don't accept those vanilla ass grayscales; ensure the range covers at least the min:
        while max(rgb) - min(rgb) < MIN_RANGE:
            colors.pop(max_color_index)
            max_color_index = get_max_color_freq_idx(colors)
            color_and_freq = colors[max_color_index]        
            rgb = color_and_freq[1]

        top_colors.append(colors.pop(max_color_index)[1])
    
    return top_colors


def get_top_color_of_verticals(verticals):
    print('in get_top_color_of_verticals')
    top_colors = []

    for vertical in verticals:
        colors = vertical.getcolors(vertical.size[0] * vertical.size[1])
        top_color_and_freq = max(colors, key = itemgetter(0))
        print('top_color: {}'.format(top_color_and_freq[1]))
        top_colors.append(top_color_and_freq[1])

    return top_colors


def get_verticals(img):
    imgwidth, imgheight = img.size
    verticals = []

    for i in range(VERTICAL_COLUMNS):
        column_lbnd = (imgwidth / VERTICAL_COLUMNS) * i
        column_rbnd = (imgwidth / VERTICAL_COLUMNS) * (i + 1)
        bbox = (column_lbnd, 0, column_rbnd, imgheight) # left, upper, right, lower boundaries of img
        slice = img.crop(bbox)
        verticals.append(slice)

    return verticals


def run() -> list:
    img = get_screenshot()
    img = img.resize(RESIZE_DIMENSIONS, Image.ANTIALIAS)
    verticals = get_verticals(img)
    print('got verticals: 0\'s height: {}, and width: {}'.format(verticals[0].height, verticals[0].width))
    top_colors = get_top_color_of_verticals(verticals)

    # Order by frequency; disregarding greyscales:
    # color_list = img.getcolors(img.size[0] * img.size[1])
    # top_colors = get_top_x_colors(color_list, NUMBER_OF_COLORS)
    # print('top_colors: {}'.format(top_colors))

    return top_colors

        