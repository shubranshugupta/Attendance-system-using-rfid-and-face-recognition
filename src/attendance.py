import face_recognition
import cv2
import numpy as np

from .utils import load_embedding
from .db import DBAttendance

class DetectFace:
    def __init__(self, frame_resizing):
        self.frame_resizing = frame_resizing

    def detect_known_faces(self, frame, roll):
        known_encodings = load_embedding(roll)

        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=2, model="large")

        face_mean_matches = []
        for face_encoding in face_encodings:
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            mean_match = np.mean(face_distances)
            face_mean_matches.append(mean_match)
        
        most_similar_face = np.array(face_mean_matches)<0.4
        if np.count_nonzero(most_similar_face) > 1:
            most_similar_face = np.array(face_mean_matches)<=np.min(face_mean_matches)

        face_mean_matches = np.where(most_similar_face, roll, "None")
        print(face_mean_matches)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_mean_matches


def attendance_via_camera(roll):

    df = DetectFace(0.5)
    cap = cv2.VideoCapture(0)

    total_found = 0
    total_not_found = 0

    while total_found < 5 and total_not_found < 100:
        ret, frame = cap.read()
        if ret:
            face_locations, face_names = df.detect_known_faces(frame, roll)
            
            if np.count_nonzero(face_names == roll) == 1:
                total_found+=1
            else:
                total_not_found+=1

            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)

            cv2.imshow('Attendance', frame)
            k=cv2.waitKey(1)
            if k & 0xFF==ord('y'):
                break
    
    cv2.destroyAllWindows()
    cap.release()

    if total_found == 5:
        DBAttendance.start()
        DBAttendance.insert(roll, True)
        DBAttendance.close()
        return True
    else:
        return False