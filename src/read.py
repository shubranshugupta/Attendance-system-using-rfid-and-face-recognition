import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read():
    try:
        print("Scan Card")
        id_, text = reader.read()
        return id_, text.strip(" ")
    except Exception as e:
        return e
    finally:
        GPIO.cleanup()

# if __name__ == "__main__":
#     print(read())