import cv2
import os
import numpy as np
import pickle
from numpy import asarray, reshape
from scipy.spatial.distance import cosine
from tensorflow.keras.preprocessing.image import smart_resize

filename = r"C:\Users\shubh\anaconda3\lib\site-packages\keras_vggface\models.py"
text = open(filename).read()
open(filename, "w+").write(text.replace('keras.engine.topology', 'tensorflow.keras.utils'))

from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from keras_vggface.utils import decode_predictions


def get_embeddings(img):
    samples = asarray(img, 'float32')
    samples = preprocess_input(samples, version=2)
    samples = smart_resize(samples, (224, 224))
    samples = reshape(samples, (1, 224, 224, 3))
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    yhat = model.predict(samples)
    return yhat

def match_score(original_embedding, face_embedding, thresh=0.5):
    score = cosine(original_embedding, face_embedding)
    if score < thresh:
        return True, score
    return False, score

def load_embedding():
    try:
        with open(os.path.join('data', 'embedding.pickle'), 'rb') as handle:
            b = pickle.load(handle)
            return b
    except FileNotFoundError:
        return {}

def save_embedding(rollNo, embedding):
    a = load_embedding()
    a[rollNo] = embedding
    print(a)
    with open(os.path.join('data', 'embedding.pickle'), 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

def main(rollNo, new_user=False, thresh=0.5):
    path = os.path.join(os.path.dirname(__file__), 'xml', 'haarcascade_frontalface_default.xml')
    model = cv2.CascadeClassifier(path)
    cap = cv2.VideoCapture(0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (0, 0, 0)
    thickness = 1

    i = 0
    while i<1:
        ret, photo = cap.read()
        if ret:
            fdetect  = model.detectMultiScale(photo)

            if len(fdetect) == 1:
                x, y, w, h = fdetect[0]
                if (w>70 and w<450) and (h>70 and h<450):
                    photo1 = cv2.rectangle(photo, (x, y), (x+w, y+h), (0, 255, 0), 1)
                    photo1 = cv2.putText(photo1, 'Press Enter to confirm', org, font, fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imshow("Face", photo)
        else:
            print('Error')
        
        if cv2.waitKey(100) == 13:
            photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
            pred_embedding = get_embeddings(photo[y:y+h, x:x+w])
            if new_user:
                save_embedding(rollNo, pred_embedding)
            else:
                orig_embedding = load_embedding()[rollNo]
                match, score = match_score(orig_embedding, pred_embedding, thresh)
                if match:
                    print('Match', score)
                else:
                    print('Not Match', score)
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main(rollNo=32130, thresh=0.4)