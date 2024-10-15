from flask import session
import keras
import cv2
from keras.models import model_from_json
# from keras.preprocessing import image
import keras.utils as image
from keras.preprocessing.image import ImageDataGenerator

import numpy as np


import face_recognition
import pickle
from datetime import datetime
from core import rec_face_image
from database import *

model = model_from_json(open(r"model\facial_expression_model_structure.json", "r").read())
model.load_weights(r'model\facial_expression_model_weights.h5')  # load weights



face_cascade = cv2.CascadeClassifier(r'model\haarcascade_frontalface_default.xml')

# cap = cv2.VideoCapture(0)


emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

def camclick(img,id1):
    # i=0
    # while(True):
        # ret, img = cap.read()

        # img = cv2.imread('../11.jpg')
        # cv2.imwrite(str(i)+".jpg",img)
        # i=i+1
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #print(faces) #locations of detected faces
    emotion=None

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image

        detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
        detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
        detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

        img_pixels = image.img_to_array(detected_face)
        img_pixels = np.expand_dims(img_pixels, axis = 0)

        img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
        
            
        predictions = model.predict(img_pixels) #store probabilities of 7 expressions

        #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
        max_index = np.argmax(predictions[0])

        emotion = emotions[max_index]
        cv2.putText(img,emotion,(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)

        
        #Save just the rectangle faces in SubRecFaces
        sub_face = img[y:y+h, x:x+w]

        FaceFileName = "static/test.jpg" #Saving the current image from the webcam for testing.
        # print("FaceFileName : ",FaceFileName)
        

        cv2.imwrite(FaceFileName, sub_face)

        # import time
        # while True:
        #     time.sleep(10)
        #     # print("10 seconds has passed")

            # break
        
        val=rec_face_image(FaceFileName)
        # print("VAL............",val)
        # print("user",val)
        str1=""
        for ele in val:  
            str1 = ele
            print(str1)
            val=str1.replace("'","")
            print("val : ",val)
            for i in val:
                print("iii : ",i)
                # q="select * from student where id='%s'" %(i)
                # res=select(q)
                # if res:
                #     session['aid']=id1
                #     session['stid']=i
                #     if emotion=='happy':
                #         q1="insert into emotiondetection values(NULL,'%s','%s','%s','%s',curdate())"%(id1,i,emotion,5)
                #         res1=insert(q1)
                #     elif emotion=='neutral':
                #         q1="insert into emotiondetection values(NULL,'%s','%s','%s','%s',curdate())"%(id1,i,emotion,4)
                #         res1=insert(q1)
                #     elif emotion=='angry':
                #         q1="insert into emotiondetection values(NULL,'%s','%s','%s','%s',curdate())"%(id1,i,emotion,2)
                #         res1=insert(q1)
                #     else:
                #         q1="insert into emotiondetection values(NULL,'%s','%s','%s','%s',curdate())"%(id1,i,emotion,1)
                #         res1=insert(q1)

                #     q2="select * from attendance where student_id='%s' and date=curdate()"%(i)
                #     print(q2)
                #     res2=select(q2)
                #     if res2:
                #         qa="update attendance set date=curdate() where student_id='%s'"%(i)
                #         update(qa)
                #     else:
                #         qb="insert into attendance values(NULL,'%s',curdate(),'present')"%(i)
                #         insert(qb)
                
                    
        # print (emotion)
        print("em")
                    # if res:
                    #     print (emotion)
                    #     valnew="Welcome "+res[0]['student_name']
                    #     # flash(valnew)
                    #     now = datetime.now()
                    #     current_time = now.strftime("%H:%M:%S")
                    #     if current_time>"09:00:00" and current_time<"09:59:00":
                    #         print("haiiss")
                    #         q="select * from attendance where student_id='%s' and date=curdate()" %(val)
                    #         print(q)
                    #         res2=select(q)
                    #         print(res)
                    #         if res2:
                    #             print("Your attendance is Already Marked")
                    #         else:
                    #             q="insert into attendance values(null,'%s',curdate(),curtime(),'Present')" %(val)
                    #             insert(q)
                    #             print("Attanadance Marked")
                    #     else:
                    #         q="select * from attendance where student_id='%s' and date=curdate()" %(val)
                    #         res2=select(q)
                    #         print(res)
                    #         if res2:
                    #             print("Your attendance is Already Marked")
                    #         else:
                    #             q="insert into attendance values(null,'%s',curdate(),curtime(),'Late')" %(val)
                    #             insert(q)
                    #             # flash("Attanadance Marked")
                    #             print("You are late")
                    #     flag=1
                    # else:
                    #     # print("No student")
                    #     print("No student")
                    #     flasg=1

        # if cv2.waitKey(1):
        #     cv2.imshow('img', img)

        # if cv2.waitKey(1) & 0xFF == ord('q'): 
        #     # for j in val:
        #     #     q2="SELECT AVG(emotions_score) as avgc FROM emotions WHERE student_id='%s'"%(j)
            #     print(q2)
            #     res2=select(q2)
            #     q3="insert into ratings values(NULL,'%s','%s','%s',curdate())"%(session['aid'],j,res2[0]['avgc'])
            #     q4="select * from ratings where assign_id='%s' and student_id='%s' and date=curdate()"%(session['aid'],j)
            #     rt=select(q4)
            #     if not rt:
            #         insert(q3) # press q to quit
            #         break
    #         break

    #     # kill open cv things
    # cap.release()
    # cv2.destroyAllWindows()
            # 	pass
        # return emotion
            #write emotion text above rectangle





# /////////////////////////////////////////
# recognize face image


def rec_face_image(imagepath):
    print("hy...........",imagepath)
    
    data = pickle.loads(open('faces.pickles', "rb").read())
    print("DATA : ",data)

    # load the input image and convert it from BGR to RGB
    image = cv2.imread(imagepath)
    print("image : ", image)
    h,w,ch=image.shape
    print("CH : ",ch)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print("RGB : ",rgb)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb,
        model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    print("encodings : ",encodings)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding,tolerance=0.4)
        print("matches : ",matches)
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

# camclick(id1=)

