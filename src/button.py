from time import time, sleep
import RPi.GPIO as GPIO
from typing import Callable

ENROLL_BUTTON = 10

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ENROLL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_loop(ids:str, callback:Callable = None):
    """
    callback function should have ids as argument
    """
    setup()
    curr_time = time()
    pressed = False

    while time() - curr_time < 10 and not pressed:
        if GPIO.input(ENROLL_BUTTON)==GPIO.LOW:
            if callback is not None:
                callback(ids=ids)

            pressed = True
            sleep(1)