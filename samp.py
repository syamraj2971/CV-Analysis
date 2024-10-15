from asyncio import Lock
import cv2
import mediapipe as mp
import requests
import numpy as np

from em import *
from DBConnection import *
from database import *
# from DBConnection import db as DB
import threading
import time 


# /////////////////////////////////////////

# import os
# from flask_cors import CORS
# from difflib import SequenceMatcher
# from flask import Flask, request, jsonify

# import joblib
# from flask_restful import reqparse
# from bson.json_util import dumps



from api import api



# from math import sqrt
# from flask import Flask, render_template, request, jsonify
# from __future__ import division
# from collections import Counter

from predict import Predictor
# from model import Model
# import pickle
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# import json
# from bson import json_util
# from PyPDF2 import PdfFileReader

# import uuid


# import os
from flask_cors import CORS
# from difflib import SequenceMatcher
# from flask import Flask, request, jsonify

import joblib
from flask_restful import reqparse

from em import *
from threading import Event
import threading
# stop_camera_event = Event()
stop_camera_event = threading.Event()
cap = None  # Declare cap as a global variable


def detection(id1):
	import cv2
	import mediapipe as mp
	import numpy as np
	

	
	global cap 
	print("___________________________________________________stage1")
	# global camera_running
	# while camera_running:
	cap = cv2.VideoCapture(0)

	mp_face_mesh = mp.solutions.face_mesh
	face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

	while not stop_camera_event.is_set():
		print("___________________________________________________stage2")

		if cap.isOpened():
			# success, image = cap.read()
			# ret, frame = cap.read()
			#++++++++++++++++++++++++++++

			

			# if cap.isOpened():
				
			# 	ret, frame = cap.read()
			# 	print(ret)
			# 	print(frame)
			# else:
			# 	ret=False
			# #+++++++++++++++++++++++++++++
			# if not ret:
			# 	break


			# with Lock:  # Use a lock for thread-safe access
			#     if not camera_running:
			#         break  
		
			mp_face_mesh = mp.solutions.face_mesh
			face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
			cap = cv2.VideoCapture(0)
			flag=0
			count=0
			text=""
			jj=-1
			path = r"static/"
			while cap.isOpened():
				success, image = cap.read()
				
				# Flip the image horizontally for a later selfie-view display
				# Also convert the color space from BGR to RGB

				image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
				#print(image,"bbbbbbbb")
				
				# To improve performance
				image.flags.writeable = False

				# Get the result
				results = face_mesh.process(image)


				# To improve performance
				image.flags.writeable = True

				# Convert the color space from RGB to BGR
				image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				
				from em import camclick
				im=camclick(image,id1)
				#print("IMM : ",im)

				img_h, img_w, img_c = image.shape
				face_3d = []
				face_2d = []

				if results.multi_face_landmarks:
					#print(len(results.multi_face_landmarks))
					jj=jj+1
					for face_landmarks in results.multi_face_landmarks:
						print (jj,"+++++++++++++++++")
						for idx, lm in enumerate(face_landmarks.landmark):
							if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
								if idx == 1:
									nose_2d = (lm.x * img_w, lm.y * img_h)
									nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

								x, y = int(lm.x * img_w), int(lm.y * img_h)

								# Get the 2D Coordinates
								face_2d.append([x, y])

								# Get the 3D Coordinates
								face_3d.append([x, y, lm.z])

								# Convert it to the NumPy array
						face_2d = np.array(face_2d, dtype=np.float64)

						# Convert it to the NumPy array
						face_3d = np.array(face_3d, dtype=np.float64)

						# The camera matrix
						focal_length = 1 * img_w

						cam_matrix = np.array([[focal_length, 0, img_h / 2],
											[0, focal_length, img_w / 2],
											[0, 0, 1]])

						# The Distance Matrix
						dist_matrix = np.zeros((4, 1), dtype=np.float64)

						# Solve PnP
						success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

						# Get rotational matrix
						rmat, jac = cv2.Rodrigues(rot_vec)

						# Get angles
						angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

						# Get the y rotation degree
						x = angles[0] * 360
						y = angles[1] * 360
						# #print(y)
						# See where the user's head tilting
						if y < -10:
							flag=1
							count=count+1
							text = "Looking Left"
						elif y > 10:
							flag = 1
							count = count + 1
							text = "Looking Right"
						elif x < -10:
							flag = 1
							count = count + 1
							text = "Looking Down"
						else:
							flag=0
							count=0
							text = "Forward"
						#print(text,"======================================")
						# # Display the nose direction
						# nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
						#
						# p1 = (int(nose_2d[0]), int(nose_2d[1]))
						# p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
						#
						# cv2.line(image, p1, p2, (255, 0, 0), 2)

						# Add the text on the image
						cv2.putText(image, text, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
						# cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				else:
					text="No Face"
					cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				#print(face_2d,"face_2d+++++++")
				if flag==1:
					if count==50:
						import time
						dt = time.strftime("%Y%m%d_%H%M%S")
						cv2.imwrite(path + "malpractice\\" + dt + ".png", image)
						pth =   dt + ".png"
						#print(pth,'//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
						# new=rec_face_image(pth)
						# insert_malpractice()
						# requests.get("http://127.0.0.1:8000/insert_malpractice/"+ dt + ".png")
						# db = DB()
						# iud(
						#     "insert into malpractice values(null,'1',curdate(),curtime(), '" + pth + "' )")
						qry="insert into malpractice values(null,'%s',curdate(),curtime(),'%s')"%(id1,pth)
						insert(qry)


						
						#print("+_+_+_+_+_+)+)+)+)+_+_+_+_+_)()_")
						count=0
						flag=0
				cv2.imshow('Head Pose Estimation', image)
				if cv2.waitKey(1) & 0xFF == 27:
					break
			cap.release()
			cv2.destroyAllWindows()  # Close OpenCV window when 'Esc' key is pressed
			break
		time.sleep(1)
		
		
    
    
	cap.release()
	
