import face_recognition as fr
import cv2
import os
import sqlite3

from .db import DBEmbedding
from .utils import save_embedding, PHOTO_FOLDER


def encoding_of_enrolled_person(roll, image_path):
	enroll_encoding=[]
	
	for file in os.listdir(image_path):
		img_path = os.path.join(image_path, file)
		img = fr.load_image_file(img_path)
		try:
			face_encodings = fr.face_encodings(img, num_jitters=10, model="large")[0]
		except IndexError:
			print("No face found in image")
			continue
		
		enroll_encoding.append(face_encodings)
	
	if len(enroll_encoding) < 5:
		return False
	else:
		save_embedding(roll, enroll_encoding)
		return True

def enroll_via_camera(roll, ids):
	cap = cv2.VideoCapture(0)
	i = 0

	folder_path = os.path.join(PHOTO_FOLDER, str(roll))
	os.makedirs(folder_path, exist_ok=True)

	while i<10:
		ret, frame = cap.read()
		if ret:
			frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
			cv2.imshow('Enrolling new attendee', frame)
			cv2.imwrite(os.path.join(folder_path, str(roll)+"_"+str(i)+'.jpg'), frame)
			i+=1
			k=cv2.waitKey(1000)
			if k & 0xFF==ord('y'):
				break
	
	cv2.destroyAllWindows()	
	cap.release()
	
	if not encoding_of_enrolled_person(roll, folder_path):
		print("Enrollment failed due to less face found of user.\nTrying Again")
		enroll_via_camera(roll, ids)
	
	try:
		DBEmbedding.start()
		DBEmbedding.insert(roll, ids)
		DBEmbedding.close()
	except sqlite3.IntegrityError:
		pass

	return True
