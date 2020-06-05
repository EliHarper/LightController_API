#!/usr/bin/env python3

# Built from direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from neopixel import *
import argparse
import time
import sys

sys.path.insert(0, "/home/pi/.local/lib/python3.7/site-packages")
from kafka import KafkaConsumer
from json import loads
from decouple import config
from PIL import ImageColor

# LED strip configuration:
LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Personal Additions: #

class Delta:
    def __init__(self, range, rate, increase=True):
        self.range = range
        self.rate = rate
        self.increase = increase


# def toRgb(hex):
#     hex = hex.lstrip('#')
#     return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))


def solidColorFromHex(strip, color, wait_ms=10):
    # Accept color as hex
    print('Setting solid color to: {}'.format(color))
    rgb_color = ImageColor.getrgb(color)
    print('Color as rgb: {}'.format(rgb_color))
    print('type of rgb_color: {}'.format(type(rgb_color)))
    print('RGB [0], [1], [2]: {}, {}, {}'.format(rgb_color[0], rgb_color[1], rgb_color[2]))
    strip.begin()

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(rgb_color[0], rgb_color[1], rgb_color[2]))
        strip.show()

def fadeBetween(strip, colors, wait_ms=10):
    for i, color in colors:
        diffR = abs(ImageColor.getrgb(color)[0] - ImageColor.getrgb(colors[i+1])[0])
        # Green + blue..
        return diffR


def makeStrip(brightness):
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(brightness), LED_CHANNEL)
    return strip


def setup():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')

    args = parser.parse_args()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')



    consumer = KafkaConsumer(
        'applyScene',
        bootstrap_servers=[config('KAFKA_URL')],
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        api_version=(0,10,1)
    )

    awaitMsgs = True

    while awaitMsgs:
        try:
            for message in consumer:
                message = message.value
                print(message)
                strip = makeStrip(message['defaultBrightness'])

                switcher = {
                    "solidColorFromHex": solidColorFromHex(strip, message['colors'][0]),
                    "fadeBetween": fadeBetween(strip, message['colors']),
                }
                switcher.get(message.functionCall, "Invalid functionCall")

        except KeyboardInterrupt:
            if args.clear:
                colorWipe(strip, Color(0, 0, 0), 10)
            sys.exit(0)
        except:
            if args.clear:
                colorWipe(strip, Color(0, 0, 0), 10)
            sys.exit(0)


if __name__ == "__main__":
    setup()