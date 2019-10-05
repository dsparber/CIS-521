############################################################
# CIS 521: R2D2-Homework 1
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

from client import DroidClient
import time
from random import shuffle
import sys,tty,os,termios

############################################################
# Section 1: Let's get Rolling
############################################################

def getkey():
     old_settings = termios.tcgetattr(sys.stdin)
     tty.setcbreak(sys.stdin.fileno())
     try:
         while True:
             b = os.read(sys.stdin.fileno(), 3).decode()
             if len(b) == 3:
                 k = ord(b[2])
             else:
                 k = ord(b)
             key_mapping = {
                 127: 'backspace',
                 10: 'return',
                 32: 'space',
                 9: 'tab',
                 27: 'esc',
                 65: 'up',
                 66: 'down',
                 67: 'right',
                 68: 'left'
             }
             return key_mapping.get(k, chr(k))
     finally:
         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.',
                    'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..',
                    'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.',
                    'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
                    'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
                    '9':'----.', '0':'-----'}

class R2D2(object):

    def __init__(self, robot):
        self.init_color_names_to_rgb()
        self.droid = DroidClient() 
        self.droid.scan() # Scan for droids.
        # Connect to your robot.
        self.droid.connect_to_droid('D2-55A2')

    def drive_square(self):
        for i in range(4):
            self.droid.roll(1, 90 * i, 1)

    def drive_rectangle(self):
        for i in range(4):
            long_side = i % 2 == 0
            self.droid.roll(1, 90 * i, 2 if long_side else 1)

    def drive_robot(self, headings):
        # E.g. to drive a pentagon:
        # headings = [0, 72, 144, 216, 288]
        for heading in headings:
            self.droid.roll(1, heading, 1)

    def drive_speedy(self, roll_commands):
        for speed, heading, duration in roll_commands:
            duration = 2 * duration if speed > 0.5 else duration
            self.droid.roll(speed, heading, duration)

    def drive_polygon(self, n, speed=0.5, duration=2):
        angle = 360 / n
        for i in range(n):
            self.droid.roll(speed, angle * i, duration)

    def init_color_names_to_rgb(self):
        color_names_to_rgb = {} 
        color_names_to_rgb['red'] = (255,0,0)
        color_names_to_rgb['orange'] = (255,165,0)
        color_names_to_rgb['yellow'] = (255,255,0)
        color_names_to_rgb['green'] = (0,128,0)
        color_names_to_rgb['blue'] = (0,0,255)
        color_names_to_rgb['indigo'] = (75,0,130)
        color_names_to_rgb['violet'] = (238,130,238)
        color_names_to_rgb['purple'] = (128,0,128)
        self.color_names_to_rgb = color_names_to_rgb
 

    def set_lights(self, color_name, which_light='both'):
        r, g, b = self.color_names_to_rgb[color_name]
        if which_light in ["front", "both"]:
            droid.set_front_LED_color(r, g, b)
        if which_light in ["back", "both"]:
            droid.set_back_LED_color(r, g, b)

    def set_colors(self, which_light='both'):
        self.set_lights("red", which_light)

    def flash_colors(self, colors, seconds=1):
        for color_name in colors:
            self.set_lights(color_name)
            time.sleep(seconds)

    def drive_with_keyboard(self, speed_increment=.1, heading_increment=45, duration=0.1):
        speed = 0
        heading = 0
        max_speed = 255
        while True:
            key = getkey()
            if key == 'esc':
                break
            elif key == 'up':
                speed += speed_increment
            elif key == 'down':
                speed -= speed_increment
            elif key == 'left':
                heading += heading_increment
            elif key == 'right':
                heading -= heading_increment

            self.droid.roll(speed, heading, duration)


    def encode_in_morse_code(self, message):
        for letter in message:
            if letter not in MORSE_CODE_DICT:
                continue

            yield MORSE_CODE_DICT[letter]

    def blink(self, length):
        droid.set_holo_projector_intensity(1)
        time.sleep(length)
        droid.set_holo_projector_intensity(0)

    def play_message(self, message, short_length=0.1, long_length=0.3, 
                     length_between_blips=0.1, length_between_letters=0.5):
        for morse_letter in self.encode_in_morse_code(message):
            for symbol in morse_letter:
                length = short_length if symbol == "." else long_length
                self.blink(length)
                time.sleep(length_between_blips)
            time.sleep(length_between_letters)

def sort_lambda(roll_commands):
    roll_commands.sort(key=lambda c: (c[2], c[1]))
