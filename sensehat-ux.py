#!/usr/bin/python
import time
import sys
import string
import ConfigParser
import subprocess
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from sys import argv

sense = SenseHat()
sense.set_rotation(0)
sense.clear()

colors = {}
R = colors['R'] = (255,0,0) # Red
O = colors['O'] = (255,165,0) # Orange
Y = colors['Y'] = (255,255,0) # Yellow
G = colors['G'] = (0,255,0) # Green
B = colors['B'] = (0,0,255) # Blue
I = colors['I'] = (111,0,255) # Indigo
V = colors['V'] = (159,0,255) # Violet
N = colors['N'] = (0,0,0) # No Color
W = colors['W'] = (255,255,255) # White

pixel_matrix_logo_default = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    W, W, B, W, W, B, W, W,
    W, W, B, W, W, B, W, W,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B
]

pixel_matrix_x = [
    R, R, N, N, N, N, R, R,
    R, R, R, N, N, R, R, R,
    N, R, R, R, R, R, R, N,
    N, N, R, R, R, R, N, N,
    N, N, R, R, R, R, N, N,
    N, R, R, R, R, R, R, N,
    R, R, R, N, N, R, R, R,
    R, R, N, N, N, N, R, R
]

pixel_matrix_happy = [
    N, N, N, N, N, N, N, G,
    N, N, N, N, N, N, G, G,
    N, N, N, N, N, G, G, G,
    N, N, N, N, N, G, G, N,
    N, G, N, N, G, G, G, N,
    G, G, G, N, G, G, N, N,
    N, G, G, G, G, N, N, N,
    N, N, G, G, G, N, N, N
]

pixel_matrix_off = [
    N, N, N, N, N, N, N, N,
    N, N, N, N, R, N, N, N,
    N, N, R, N, R, N, R, N,
    N, R, N, N, R, N, N, R,
    N, R, N, N, N, N, N, R,
    N, N, R, N, N, N, R, N,
    N, N, N, R, R, R, N, N,
    N, N, N, N, N, N, N, N
]

pixel_matrix_on = [
    N, N, N, N, N, N, N, N,
    N, N, N, N, G, N, N, N,
    N, N, G, N, G, N, G, N,
    N, G, N, N, G, N, N, G,
    N, G, N, N, N, N, N, G,
    N, N, G, N, N, N, G, N,
    N, N, N, G, G, G, N, N,
    N, N, N, N, N, N, N, N
]

pixel_matrix_err = [
    N, N, O, O, O, O, O, N,
    N, N, O, O, O, O, O, N,
    N, N, N, N, N, O, O, N,
    N, N, N, N, O, O, N, N,
    N, N, N, O, O, N, N, N,
    N, N, N, O, O, N, N, N,
    N, N, N, N, N, N, N, N,
    N, N, N, O, O, N, N, N
]

MODE_WAIT = 1
MODE_SELECT = 2

mode = MODE_WAIT
start_flag = 0
options_idx = 0

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

def loadConfig():
    services = []

    sections = Config.sections()
    for section in sections:
        if section == 'init':
            continue

        service = {}
        service['name'] = section

        options = Config.options(section)
        for option in options:
            service[option] = Config.get(section, option)
	services.append(service)

    return services

def translatePixelArray(arr):
    for x, p in enumerate(arr):
        arr[x] = colors[p.strip('\t\n\r')]

    return arr

def optionInc(options_idx):
    if options_idx == len(options) - 1:
       options_idx = 0;
    else:
        options_idx = options_idx + 1;

    return options_idx

def optionDec(options_idx):
    if options_idx == 0:
        options_idx = len(options) - 1
    else:
        options_idx = options_idx - 1

    return options_idx

def processStatus(idx):
    try:
        res = int(subprocess.check_output(options[idx]["status"], shell=True))
    except subprocess.CalledProcessError:
        print("Status command failed for {}".format(options[idx]["name"]))
        res = -1

    return res

def processStart(idx):
    try:
        subprocess.check_call(options[idx]["start"], shell=True)
        return True
    except subprocess.CalledProcessError:
        print("Start failed for {}".format(options[idx]["name"]))
        return False

def processStop(idx):
    try:
        subprocess.check_call(string.split(options[idx]["stop"], " "))
        return True
    except subprocess.CalledProcessError:
        print("Stop failed for {}".format(options[idx]["name"]))
    return False

def showCurrentOption():
    status = processStatus(options_idx)
    sense.show_message(options[options_idx]["name"], 0.05)
    if status > 0:
        sense.set_pixels(pixel_matrix_on)
    elif status == 0:
        sense.set_pixels(pixel_matrix_off)
    else:
        sense.set_pixels(pixel_matrix_err)

def toggleCurrentOption():
    status = processStatus(options_idx)
    sense.clear()
    if status > 0:
        res = processStop(options_idx)
	if res == True:
            sense.set_pixels(pixel_matrix_off)
        else:
            sense.set_pixels(pixel_matrix_err)
    elif status == 0:
        if processStart(options_idx) == True:
            sense.set_pixels(pixel_matrix_on)
        else:
	    sense.set_pixels(pixel_matrix_err)
    else:
        sense.set_pixels(pixel_matrix_err)

## Main

args = getopts(argv)
if '-c' in args:
    Config = ConfigParser.ConfigParser()
    Config.read(args['-c'])

    custom_boot_logo = pixel_matrix_logo_default
    try:
        custom_boot_logo = translatePixelArray(Config.get('init', 'bootlogo').split(','))
    except ConfigParser.NoSectionError:
        pass

    options = loadConfig()
else:
   print("No config file in input.")
   sys.exit(1)

try:
    sense.set_pixels(custom_boot_logo)
except ValueError:
    print("Invalid custom boot logo.")
    sense.set_pixels(pixel_matrix_logo_default)

time.sleep(1)
sense.clear()

lastEvent = ""
while True:
    for event in sense.stick.get_events():
        thisEvent = "{}".format(event.direction)
	if mode == MODE_WAIT:
            #print("The joystick was {} {}".format(event.action, event.direction))
            if event.direction == "down" and event.action == ACTION_HELD:
                start_flag = start_flag + 1
                if start_flag > 5:
                    sense.set_pixels(pixel_matrix_happy)
                    start_flag = 0
                    mode = MODE_SELECT
                    time.sleep(1)
                    sense.clear()
            else:
                start_flag = 0
		if lastEvent != thisEvent:
                    sense.set_pixels(pixel_matrix_x)
                    time.sleep(1)
                    sense.clear()
        else:
            if event.direction == "up" and event.action == ACTION_HELD:
                start_flag = start_flag  + 1
                if start_flag > 5:
                    sense.set_pixels(pixel_matrix_happy)
                    start_flag = 0
                    mode = MODE_WAIT
                    time.sleep(1)
                    sense.clear()
            elif event.direction == "right" and event.action == ACTION_PRESSED:
                options_idx = optionInc(options_idx)
                showCurrentOption()
            elif event.direction == "left" and event.action == ACTION_PRESSED:
                options_idx = optionDec(options_idx)
                showCurrentOption()
            elif event.direction == "middle" and event.action == ACTION_PRESSED:
                toggleCurrentOption()

	lastEvent = thisEvent
    time.sleep(0.05)
