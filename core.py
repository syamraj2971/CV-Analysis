from DBConnection import *
from flask import *
import demjson
import numpy as np
from model_manager import Model
import pickle
import math
import cv2
import uuid

import face_recognition
import argparse

from imutils import paths
import os
import requests
import io
import json
from DBConnection import *
from datetime import datetime

def get_max_login_id():
	q = "select max(login_id) as  max from login"
	res = selectone(q)
	# print(res[0]['max'])
	if res:
		return res[0]['max']
	else:
		return 0

def create_matrix():
	max_id = get_max_login_id()
	matrix = []
	for i in range(0,max_id+1):
		row = []
		for j in range(0,max_id+1):
			m = Model(i,j)
			row.append(m)
		matrix.append(row)
	for i in range(0,max_id+1):
		for j in range(0,max_id+1):
			matrix[j][i] = matrix[i][j]
	return matrix


def pre_process_features(features):
	# print(features)
	temp = []
	for f in features:

		if len(f) == 6 and None not in f:
			temp.append(f)

	if temp:
		temp = temp / np.max(temp)
		temp = np.asarray(temp)
	return np.asarray(features)


def train_matrix(matrix,user1,user2):
	user_1_id = user1['login_id']
	user_2_id = user2['login_id']
	# print((user1['features']))
	# print((user2['features']))

	user_1_features = pre_process_features(demjson.decode(user1['features']))
	user_2_features = pre_process_features(demjson.decode(user2['features']))

	user_1_op = np.asarray([user_1_id] * user_1_features.shape[0])
	user_2_op = np.asarray([user_2_id] * user_2_features.shape[0])
	# X_train = np.append(user_1_features,user_2_features,axis=0)
	# Y_train = np.concatenate((user_1_op,user_2_op),axis=0)
	matrix[user_1_id][user_2_id].train(user_1_features,user_2_features,user_1_op,user_2_op)
	matrix[user_2_id][user_1_id].train(user_1_features,user_2_features,user_1_op,user_2_op)



def train():
	matrix = create_matrix()
	q = "select * from login"
	res = selectall(q)
	for i in range((len(res))):
		for j in range((len(res))):
			user1 = res[i]
			user2 = res[j]
			train_matrix(matrix,user1,user2)
	file = open("model.pickle","wb")
	pickle.dump(matrix,file)
	file.close()


def predict(matrix,id1,id2,features):

	# print(features)
	
	if id1 > -1 and id2 > -1:
		res = matrix[id2][id1].predict(features)
		print(matrix[id2][id1])
	elif id1 > -1:
		res = id1
	elif id2 > -1:
		res = id2
	else:
		res = -1
	# print(res)
	# prob = matrix[id2][id1].predict_proba(features)
	# print(prob)

	return res

def predict_from_array(matrix,array,features):
	# print(array)
	new_layer = []
	if len(array) > 1:

		for i in range((len(array) - 1)):
			user1 = array[i]
			user2 = array[i+1]

			new_layer.append(predict(matrix,user1,user2,features))

		if len(new_layer) == 1:
			return new_layer[0]
	else:
		user1 = array[0]
		user2 = array[0]
		# print(features)
		return predict(matrix,user1,user2,features)
	return predict_from_array(matrix,new_layer,features)




def get_login_id(features):
	file = open("model.pickle","rb")
	matrix = pickle.load(file)
	file.close()
	features = pre_process_features(demjson.decode(features))

	q = "select * from login"
	res = selectall(q)
	layer = []
	for row in res:
		layer.append(row['login_id'])

	id = predict_from_array(matrix,layer,features)
	return id
# train()
# features = "[[64,58,407,401,465,343],[58,82,446,470,528,388],[82,78,427,423,505,345],[78,112,295,329,407,217],[112,73,535,496,608,423],[73,83,461,471,544,388],[83,87,477,481,564,394],[87,56,441,410,497,354],[56,71,1008,1023,1079,952],[71,69,573,571,642,502],[69,112,270,313,382,201],[112,98,634,620,732,522],[98,73,1084,1059,1157,986],[73,83,260,270,343,187],[83,119,371,407,490,288],[119,133,412,426,545,293],[133,118,362,347,480,229],[118,137,270,289,407,152],[137,82,335,280,417,198],[82,111,331,360,442,249],[111,116,303,308,419,192],[116,143,390,417,533,274],[143,103,217,177,320,74],[103,108,358,363,466,255],[108,90,411,393,501,303],[90,111,266,287,377,176],[111,120,297,306,417,186],[120,117,269,266,386,149],[117,100,346,329,446,229],[100,101,228,229,329,128],[101,98,326,323,424,225],[98,111,365,378,476,267],[111,119,429,437,548,318],[119,85,607,573,692,488],[85,88,695,698,783,610],[88,99,358,369,457,270],[99,105,291,297,396,192],[105,140,530,565,670,425],[140,160,183,203,343,43],[160,106,350,296,456,190],[106,78,709,681,787,603],[78,109,422,453,531,344],[109,131,212,234,343,103],[131,105,337,311,442,206],[105,119,284,298,403,179],[119,95,292,268,387,173],[95,128,218,251,346,123],[128,131,234,237,365,106],[131,87,176,132,263,45],[87,65,511,489,576,424],[65,102,153,190,255,88],[102,105,270,273,375,168],[105,63,263,221,326,158],[63,127,268,332,395,205],[127,88,347,308,435,220],[88,88,275,275,363,187],[88,104,198,214,302,110],[104,118,226,240,344,122],[118,117,205,204,322,87],[117,121,340,344,461,223],[121,118,209,206,327,88],[118,141,265,288,406,147],[141,76,495,430,571,354],[76,106,154,184,260,78],[106,111,318,323,429,212],[111,88,256,233,344,145],[88,99,210,221,309,122],[99,91,261,253,352,162],[91,108,662,679,770,571],[108,77,456,425,533,348],[77,81,272,276,353,195],[81,122,189,230,311,108],[122,143,250,271,393,128],[143,100,265,222,365,122],[100,107,252,259,359,152],[107,134,349,376,483,242],[134,120,588,574,708,454],[120,78,587,545,665,467],[78,69,458,449,527,380],[69,86,578,595,664,509],[86,84,623,621,707,537],[84,107,333,356,440,249],[107,93,545,531,638,438],[93,83,441,431,524,348],[83,77,385,379,462,302],[77,72,233,228,305,156],[72,122,81,131,203,9],[122,81,206,165,287,84],[81,116,355,390,471,274],[116,76,911,871,987,795],[76,101,185,210,286,109],[101,108,215,222,323,114],[108,130,212,234,342,104],[130,124,192,186,316,62],[124,124,209,209,333,85],[124,96,233,205,329,109],[96,118,150,172,268,54],[118,149,169,200,318,51],[149,111,287,249,398,138],[111,136,304,329,440,193],[136,80,682,626,762,546],[80,100,204,224,304,124],[100,86,268,254,354,168],[86,108,164,186,272,78],[108,95,263,250,358,155],[95,110,193,208,303,98],[110,88,254,232,342,144],[88,83,238,233,321,150],[83,111,255,283,366,172],[111,95,236,220,331,125],[95,90,304,299,394,209],[90,89,196,195,285,106],[89,81,284,276,365,195],[81,105,236,260,341,155],[105,108,183,186,291,78],[108,82,290,264,372,182],[82,94,204,216,298,122],[94,71,358,335,429,264]]"
# id = get_login_id(features)

# print(id)


# //////////////////////////////////////////////////////////////////////
# camera for image testing
def val():
	size = 4


	# We load the xml file
	classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

	webcam = cv2.VideoCapture(0) #Using default WebCam connected to the PC.
	(rval, im) = webcam.read()
	flag=0
	while True:
		(rval, im) = webcam.read()
		im=cv2.flip(im,1,0) #Flip to act as a mirror

		# Resize the image to speed up detection
		mini = cv2.resize(im, (int(im.shape[1]/size), int(im.shape[0]/size)))

		# detect MultiScale / faces 
		faces = classifier.detectMultiScale(mini)

		# Draw rectangles around each face
		flag=0
		for f in faces:
			(x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
			cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 4)

			#Save just the rectangle faces in SubRecFaces
			sub_face = im[y:y+h, x:x+w]

			FaceFileName = "static/test.jpg" #Saving the current image from the webcam for testing.
			

			cv2.imwrite(FaceFileName, sub_face)
	
			# break
			val=rec_face_image(FaceFileName)
			# print(val)
			# print("user",vals)
			str1=""
			for ele in val:  
				str1 = ele
			# print(str1)
			val=str1.replace("'","")
			# print("val : ",val)
			q="select * from staff where staff_id='%s'" %(val)
			res=selectall(q)
			if res:
				valnew="Welcome "+res[0]['first_name']
				flash(valnew)
				now = datetime.now()
				current_time = now.strftime("%H:%M:%S")
				if current_time>"09:00:00" and current_time<"09:59:00":
					# print("haiiss")
					q="select * from attendance where staff_id='%s' and date=curdate()" %(val)
					# print(q)
					res2=selectall(q)
					# print(res)
					if res2:
						flash("Your attendance is Already Marked")
					else:
						q="insert into attendance values(null,%s,curdate(),curtime(),'Present')" %(val)
						val=(val)
						iud(q,val)
						flash("Attanadance Marked")
				else:
					q="select * from attendance where staff_id='%s' and date=curdate()" %(val)
					res2=selectall(q)
					# print(res)
					if res2:
						flash("Your attendance is Already Marked")
					else:
						q="insert into attendance values(null,'%s',curdate(),curtime(),'Late')" %(val)
						val=(val)
						iud(q)
						# flash("Attanadance Marked")
						flash("You are late")
				flag=1
			else:
				# print("No Staff")
				flash("No Staff")
				flasg=1


			# if val!="":
				
			# 	q="SELECT * FROM journey where passenger_id='%s' and ending_station_id='0'"%(str(val))
			# 	res=select(q)
			# 	if res:
			# 		ssid=res[0]['starting_station_id']
			# 		jouid=res[0]['journey_id']
			# 		if(str(res[0]['starting_station_id'])==str(session['station_id'])):
			# 			print("same station")
			# 			q="SELECT * FROM passengers where passenger_id='%s'"%(str(val))
			# 			res=select(q)
			# 			if res:
			# 				pname= res[0]['first_name']+" "+ res[0]['last_name']
			# 				cv2.putText(im,pname, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
				
			# 		else:
			# 			q="SELECT * FROM passengers where passenger_id='%s'"%(str(val))
			# 			res=select(q)
			# 			if res:
			# 				pname= res[0]['first_name']+" "+ res[0]['last_name']
			# 				cv2.putText(im,pname, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
						
			# 			esid=session["station_id"]
			# 			q="SELECT * FROM stations where station_id='%s'"%(ssid)
			# 			res=select(q)
			# 			s1=res[0]['station_order_no']
			# 			q="SELECT * FROM stations where station_id='%s'"%(esid)
			# 			res=select(q)
			# 			s2=res[0]['station_order_no']
			# 			sno=int(s2)-int(s1)
			# 			print(sno)
			# 			sno=str(sno)
			# 			sno1=sno.replace("-", "")
			# 			sno1=int(sno1)+1
			# 			print(sno1)

			# 			q="SELECT * FROM fares where no_of_stations='%s'"%(sno1)
			# 			res=select(q)
			# 			if res:
			# 				fair=res[0]['amount']
			# 			else:
			# 				flash("Please add fair...")
			# 			print("fair:"+fair)
			# 			q="SELECT * FROM wallet where passenger_id='%s'"%(str(val))
			# 			res=select(q)
			# 			if res:
			# 				fairamt=res[0]['amount']
			# 				fairamount=float(fairamt)-float(fair)
			# 				q="update wallet set amount='%s' where passenger_id='%s'"%(str(fairamount),str(val))
			# 				id=update(q)
			# 				q="insert into payments values(NULL,'%s','%s',now())"%(jouid,fair)
			# 				id=insert(q)
			# 			else:
			# 				flash("Please add fair/recharge wallet...")
			# 			q="update journey set ending_station_id='%s',ending_date_time=now() where passenger_id='%s' and ending_station_id='0'"%(session["station_id"],str(val))
			# 			id=update(q)
			# 			flash("journey end and the amount deducted from your wallet...")

			# 			flag=1

			# 	else:
			# 		q="SELECT * FROM passengers where passenger_id='%s'"%(str(val))
			# 		res=select(q)
			# 		if res:
			# 			pname= res[0]['first_name']+" "+ res[0]['last_name']
			# 			cv2.putText(im,pname, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
			
			# 		path='static/uploads/img'+str(uuid.uuid4())+".jpg"
			# 		cv2.imwrite(path, sub_face) 
		
			# 		q="INSERT INTO journey VALUES(NULL,'%s','%s','%s',now(),'0','pending')" %(str(val),path,session["station_id"])
			# 		insert(q)
			# 		flash("Face recognized Start Journey...")
			# 		flag=1
					
					
					
		cv2.imshow('Capture(Press Esc to exit)',   im)
		key = cv2.waitKey(10)
		# print("key : ",key)
		# # if Esc key is press then break out of the loop 
		if key == 27: #The Esc key
			break
			return "failed"

		if flag==1:
			break
			
	

# /////////////////////////////////////////
# recognize face image


def rec_face_image(imagepath):
    # print(imagepath)

    data = pickle.loads(open('faces.pickles', "rb").read())

    # load the input image and convert it from BGR to RGB
    image = cv2.imread(imagepath)
    #print(image)
    h,w,ch=image.shape
    # print(ch)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    # print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb,
        model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding,tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:

                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            print(counts, " rount ")
            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            if len(counts) == 1:
                name = max(counts, key=counts.get)
            else:
                name = "-1"
        # update the list of names
        # if name not in names:
        if name != "Unknown":
            names.append(name)
    return names


# ////////////////////////////////////////////////////////
# image write or uploads

def enf(path):
        imagePaths = path

	# initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []
        for  fname in os.listdir(imagePaths):
            facedir=os.path.join(imagePaths,fname)
            for  imagePt in os.listdir(facedir):
                img=os.path.join(facedir,imagePt)
		# extract the person name from the image path
                # print("[INFO] processing image {}/{}".format(fname,len(imagePt)))
                # print("imagepath-------",imagePaths)
                # print(magePath.split(os.path.sep))
               
                name = fname
                 
                # load the input image and convert it from RGB (OpenCV ordering)
                # to dlib ordering (RGB)

                image = cv2.imread(img)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # detect the (x, y)-coordnates of the bounding boxes
                # corresponding to each face in the input image
                boxes = face_recognition.face_locations(rgb,model='hog')

		# compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # loop over the encodings
                for encoding in encodings:
                        # add each encoding + name to our set of known names and
                        # encodings
                        knownEncodings.append(encoding)
                        knownNames.append(name)

        # dump the facial encodings + names to disk
        # print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open('faces.pickles', "wb")
        f.write(pickle.dumps(data))
        f.close()

# //////////////////////////////////////////////////
# OCR 
def ocrgenerate(image):
	print(image)
	img = cv2.imread(image)
	height, width, _ = img.shape

	# Cutting image
	# roi = img[0: height, 400: width]
	roi = img

	# Ocr
	url_api = "https://api.ocr.space/parse/image"
	_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
	file_bytes = io.BytesIO(compressedimage)

	result = requests.post(url_api,
	              files = {"screenshot.jpg": file_bytes},
	              data = {"apikey": "f2c63a5eb288957",
	                      "language": "eng"})

	result = result.content.decode()
	result = json.loads(result)
	# print(result)
	parsed_results = result.get("ParsedResults")[0]
	text_detected = parsed_results.get("ParsedText")
	# print(text_detected)

	# cv2.imshow("roi", roi)
	# cv2.imshow("Img", img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return text_detected



