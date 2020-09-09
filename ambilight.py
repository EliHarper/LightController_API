from operator import itemgetter
from PIL import ImageGrab, Image
import time
import gc


MIN_RANGE = 10
NUMBER_OF_COLORS = 5
RESIZE_DIMENSIONS = (150,150)



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


def run() -> list:
# if __name__ == '__main__':
#     while True:
    img = get_screenshot()
    img = img.resize(RESIZE_DIMENSIONS, Image.ANTIALIAS)
    color_list = img.getcolors(img.size[0] * img.size[1])
    top_colors = get_top_x_colors(color_list, NUMBER_OF_COLORS)

    return top_colors

        