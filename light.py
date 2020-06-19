#!/usr/bin/env python3

# Built from direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from neopixel import *
import threading
import argparse
import time
import sys

sys.path.insert(0, "/home/pi/.local/lib/python3.7/site-packages")
from kafka import KafkaConsumer
from json import loads
from decouple import config
from multiprocessing import Process
import traceback

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

# Helpers:
class Delta:
    def __init__(self, range, rate, increase=True):
        self.range = range
        self.rate = rate
        self.increase = increase


def convert_to_rgb(colors):
    tupleys = []
    for hex_color in colors:
        hex_color = hex_color.lstrip('#')
        tupleys.append(tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))

    return tupleys

# Action functions:
# Administrative:
def create_kafka_consumer():
    return KafkaConsumer(
        'applyScene',
        bootstrap_servers=[config('KAFKA_URL')],
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        api_version=(0,10,1)
    )


def turn_off(strip):
    colorWipe(strip, Color(0,0,0), 10)


def make_strip(brightness):
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(brightness), LED_CHANNEL)
    return strip


def animation_handler(strip, colors, animation):
    global stop_animation
    while not stop_animation:
        switcher = {
            "Projectile": fire_projectiles,
            "Breathe": breathe,
        }
        switcher[animation](strip, colors)


def handle_ending_animation(strip, message):
    global stop_animation
    # Short-circuit in the event of a "turn off" message:
    if message['functionCall'] == "off":
        if strip is not None:
            stop_animation = True
            print('Received call for turn_off')
            print(stop_animation)
            turn_off(strip)
            scene.join()
            stop_animation = False
            # Returning False tells the main loop to just wait for the next message
            #   instead of handling it further as if it were a scene
            return False
    else:
        try:
            # Check if the changed-to scene is the same as the last - if not, tell the thread to end.
            if prev_message['_id']['$oid'] == message['_id']['$oid']:
                # Don't bother with re-applying the same scene:
                return False
            else:
                if prev_message['animated']:
                    # Tell animated function to end, then wait for it to do so before continuing.
                    stop_animation = True
                    scene.join()
                    stop_animation = False

                return True
        # If animation_id is unset (first animation since app start), initialize stop_animation to False:
        except NameError:
            stop_animation = False
            return True



# Scenes:
def paint_with_colors(strip, colors):
    # Accept color as hex
    print('Setting solid color to: {}'.format(colors))
    # Extracting ints from RgbColor object, which stores them as strings
    rgb_tuples = convert_to_rgb(colors)
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


def fire_projectiles(strip, colors, projectile_size=8, fractional_distance=2):
    global stop_animation
    rgb_tuples = convert_to_rgb(colors)

    while not stop_animation:
        for index in (0, len(rgb_tuples), fractional_distance):
            if stop_animation or index >= len(rgb_tuples) - 1:
                break
            fire_one(strip, rgb_tuples, index, projectile_size, fractional_distance)


def fire_one(strip, rgb_tuples, index, projectile_size, fractional_distance):
    red, green, blue = rgb_tuples[index]
    for i in range(strip.numPixels()):
        if i == (strip.numPixels() / fractional_distance) and index <= len(rgb_tuples) - 2:
            firing = Process(target=fire_one, args=(strip, rgb_tuples, index + 1, projectile_size, fractional_distance))
            firing.start()
        strip.setPixelColor(i, Color(green, red, blue))
        strip.show()
        # i => head of projectile
        if i > (projectile_size - 1):
            strip.setPixelColor(i - projectile_size, Color(0, 0, 0))


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


def fade_between(strip, colors, wait_ms=10):
    for i, color in colors:
        diffR = abs(hex(color)[0] - hex(colors[i+1])[0])
        # Repeat for green + blue..
        return diffR




def run():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')

    args = parser.parse_args()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    consumer = create_kafka_consumer()

    await_msgs = True
    strip = None

    global prev_message
    global scene
    global stop_animation

    while await_msgs:
        try:
            for message in consumer:
                message = message.value
                print(message)
                print(message['functionCall'])

                if not handle_ending_animation(strip, message):
                    break

                if strip is None:
                    strip = make_strip(message['defaultBrightness'])
                    strip.begin()
                else:
                    strip.setBrightness(int(message['defaultBrightness']))

                if message['animated']:
                    scene = threading.Thread(target = animation_handler, args=(strip, message['colors'], message['animation']))
                else:
                    scene = threading.Thread(target = paint_with_colors, args=(strip, message['colors']))

                scene.start()
                prev_message = message


        except KeyboardInterrupt:
            if args.clear:
                colorWipe(strip, Color(0, 0, 0), 10)
            sys.exit(0)
        except Exception as e:
            print(e)
            exc_info = sys.exc_info()
            # Display the *original* exception
            traceback.print_exception(*exc_info)
            del exc_info
            if args.clear:
                colorWipe(strip, Color(0, 0, 0), 10)
            sys.exit(0)


if __name__ == "__main__":
    run()