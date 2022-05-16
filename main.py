from src.enroll import enroll_via_camera
from src.attendance import attendance_via_camera
from src.read import read
from src.write import write
from src.utils import setup
from src.button import button_loop
from src.db import DBEmbedding

import RPi.GPIO as GPIO


def button_callback(ids):
    print("Button Pressed ", ids)
    roll = write()
    enroll_via_camera(roll, ids)

if __name__ == '__main__':
    setup()

    try:
        while True:
            ids, rollNo = read()
            print(ids, rollNo)

            DBEmbedding.start()
            enroll = True if DBEmbedding.find_roll(rollNo) is None else False
            DBEmbedding.close()
            if enroll:
                print("Press Button To enroll")
                button_loop(ids, button_callback)
            else:
                attendance_via_camera(rollNo)
    except Exception as e:
        print(e)
        GPIO.cleanup()