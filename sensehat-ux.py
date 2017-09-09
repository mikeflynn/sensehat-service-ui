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

red = R = (255, 0, 0)
blue = L = (0, 0, 255)
black = B = (0, 0, 0)
white = W = (255, 255, 255)
green = G = (0, 255, 0)
orange = O = (255,165,0)

pixel_matrix_logo = [
    L, L, L, L, L, L, L, L,
    L, L, L, L, L, L, L, L,
    L, L, L, L, L, L, L, L,
    W, W, L, W, W, L, W, W,
    W, W, L, W, W, L, W, W,
    L, L, L, L, L, L, L, L,
    L, L, L, L, L, L, L, L,
    L, L, L, L, L, L, L, L
]

pixel_matrix_x = [
    R, R, B, B, B, B, R, R,
    R, R, R, B, B, R, R, R,
    B, R, R, R, R, R, R, B,
    B, B, R, R, R, R, B, B,
    B, B, R, R, R, R, B, B,
    B, R, R, R, R, R, R, B,
    R, R, R, B, B, R, R, R,
    R, R, B, B, B, B, R, R
]

pixel_matrix_happy = [
    B, B, B, B, B, B, B, G,
    B, B, B, B, B, B, G, G,
    B, B, B, B, B, G, G, G,
    B, B, B, B, B, G, G, B,
    B, G, B, B, G, G, G, B,
    G, G, G, B, G, G, B, B,
    B, G, G, G, G, B, B, B,
    B, B, G, G, G, B, B, B
]

pixel_matrix_off = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, R, B, B, B,
    B, B, R, B, R, B, R, B,
    B, R, B, B, R, B, B, R,
    B, R, B, B, B, B, B, R,
    B, B, R, B, B, B, R, B,
    B, B, B, R, R, R, B, B,
    B, B, B, B, B, B, B, B
]

pixel_matrix_on = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, G, B, B, B,
    B, B, G, B, G, B, G, B,
    B, G, B, B, G, B, B, G,
    B, G, B, B, B, B, B, G,
    B, B, G, B, B, B, G, B,
    B, B, B, G, G, G, B, B,
    B, B, B, B, B, B, B, B
]

pixel_matrix_err = [
    B, B, O, O, O, O, O, B,
    B, B, O, O, O, O, O, B,
    B, B, B, B, B, O, O, B,
    B, B, B, B, O, O, B, B,
    B, B, B, O, O, B, B, B,
    B, B, B, O, O, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, O, O, B, B, B
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

    try:
        pixel_matrix_logo = Config.get('init', 'bootlogo')
    except ConfigParser.NoSectionError:
        pass

    options = loadConfig()
else:
   print("No config file in input.")
   sys.exit(1)

sense.set_pixels(pixel_matrix_logo)
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
