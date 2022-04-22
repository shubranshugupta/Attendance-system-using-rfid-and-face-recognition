import pickle
import os
from os.path import dirname

ROOT_FOLDER = dirname(dirname(os.path.abspath(__file__)))
FACIAL_ENCODINGS = os.path.join(ROOT_FOLDER, "data", "encoding.pickel")
PHOTO_FOLDER = os.path.join(ROOT_FOLDER, "data", "images")
NULL_STR = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


def setup():
    os.makedirs(os.path.join(ROOT_FOLDER, "data"), exist_ok=True)
    os.makedirs(os.path.join(ROOT_FOLDER, "data", "images"), exist_ok=True)

    if not os.path.exists(os.path.join(ROOT_FOLDER, "data", "database.sqlite")):
        with open(os.path.join(ROOT_FOLDER, "data", "database.sqlite"), 'w') as handle:
            pass
    
    if not os.path.exists(FACIAL_ENCODINGS):
        with open(FACIAL_ENCODINGS, 'wb') as handle:
            pickle.dump({}, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

def load_embedding(rollNo=None):
    with open(FACIAL_ENCODINGS, 'rb') as handle:
        b = pickle.load(handle)

    if rollNo is not None:
        return b[rollNo]
    return b


def save_embedding(rollNo, embedding):
    a = load_embedding()
    print(a)
    a[str(rollNo)] = embedding
    print(a)
    with open(FACIAL_ENCODINGS, 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)