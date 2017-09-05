#!/usr/bin/python
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

sense = SenseHat()
sense.set_rotation(0)
sense.clear()

red = R = (255, 0, 0)
blue = Bl = (0, 0, 255)
black = B = (0, 0, 0)
white = W = (255, 255, 255)
green = G = (0, 255, 0)

pixel_matrix_logo = [
    R, R, R, R, R, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, W, W, R, R, R,
    R, W, W, W, W, W, W, R,
    R, W, W, W, W, W, W, R,
    R, R, R, W, W, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, R, R, R, R, R
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
        B, B, B, B, B, B, B, B,
        B, B, G, B, B, G, B, B,
        B, B, G, B, B, G, B, B,
        B, B, B, B, B, B, B, B,
        B, G, B, B, B, B, G, B,
        B, B, G, B, B, G, B, B,
        B, B, B, G, G, B, B, B,
        B, B, B, B, B, B, B, B
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

MODE_WAIT = 1
MODE_SELECT = 2

mode = MODE_WAIT
start_flag = 0

options = [
        {"name": "Access Point", "start": "...", "stop": "...", "status": False},
        {"name": "Motion Sensor", "start": "...", "stop": "...", "status": False},
        {"name": "Fruity WiFi", "start": "...", "stop": "...", "status": False}
]
options_idx = 0

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

def showCurrentOption():
    sense.show_message(options[options_idx]["name"], 0.05)
    sense.set_pixels(pixel_matrix_off)

def toggleCurrentOption():
    sense.set_pixels(pixel_matrix_on)

sense.set_pixels(pixel_matrix_logo)
time.sleep(1)
sense.clear()

while True:
    for event in sense.stick.get_events():
        if mode == MODE_WAIT:
            #print("The joystick was {} {}".format(event.action, event.direction))
            if event.direction == "down" and event.action == ACTION_HELD:
                start_flag = start_flag + 1
                if start_flag > 5:
                    #sense.show_message(":)")
                    sense.set_pixels(pixel_matrix_happy)
                    start_flag = 0
                    mode = MODE_SELECT
                    time.sleep(1)
                    sense.clear()
            else:
                sense.set_pixels(pixel_matrix_x)
                start_flag = 0
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
