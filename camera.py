import face_recognition
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import datetime
d=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
img_counter = 0
path=r"D:\riss own projects\jcet\malpractice\malpractice\src\static\\"
# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame  = vs.read()
    frame = imutils.resize(frame,width=400)
    imgname = path+"h3.jpg".format(img_counter)
    cv2.imwrite(imgname, frame)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()


from PIL import Image
from DBConnection import *
qry = "select * from criminal"

res = selectall(qry)
known_faces = []
userids = []
person_name = []
identified = []
if res is not None:
    for result in res:
        picc = result["image"]
        pname = picc.split("/")
        img = path + pname[len(pname) - 1]
        print(img)
        b_img = face_recognition.load_image_file(img)
        b_imgs = face_recognition.face_encodings(b_img)[0]
        known_faces.append(b_imgs)
        userids.append(result["criminal_id"])
        person_name.append(result["criminal_name"])
        print(str(len(known_faces)) + "done")

    # unknown_image = face_recognition.load_image_file(staticpath + "a_270.jpg")
    unknown_image = face_recognition.load_image_file(path + "h3.jpg")
    unkonownpersons = face_recognition.face_encodings(unknown_image)
    print(len(unkonownpersons), "llllllllllllllllllllllll")
    if len(unkonownpersons) > 0:
        for i in range(0, len(unkonownpersons)):
            h = unkonownpersons[i]
            red = face_recognition.compare_faces(known_faces, h, tolerance=0.45)  # true,false,false,false]
            print(red)
            for i in range(0, len(red)):
                if red[i] == True:
                    identified.append(userids[i])
        print(identified,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        l=identified





