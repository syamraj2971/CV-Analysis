import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
import cv2
import mediapipe as mp
import requests
import numpy as np
from DBConnection import *
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
flag=0
count=0
text=""
jj=-1
path = r"static/"
# For static images:
IMAGE_FILES = []
# model_selection=1,
# with mp_face_detection.FaceDetection(
#      min_detection_confidence=0.5) as face_detection:
#   for idx, file in enumerate(IMAGE_FILES):
#     image = cv2.imread(file)
#     # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
#     results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
#     # Draw face detections of each face.
#     if not results.detections:
#       continue
#     annotated_image = image.copy()
#     for detection in results.detections:
#       print('Nose tip:')
#       print(mp_face_detection.get_key_point(
#           detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
#       mp_drawing.draw_detection(annotated_image, detection)
#     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# For webcam input:
cap = cv2.VideoCapture(0)
# model_selection=0,
with mp_face_detection.FaceDetection(
     min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    imgg = image
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    # Draw the face detection annotations on the image.
    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      for detection in results.detections:
        try:
          mp_drawing.draw_detection(image, detection)
          height, width = imgg.shape[:2]
          x=int(width*detection.location_data.relative_bounding_box.xmin)
          y=int(height*detection.location_data.relative_bounding_box.ymin)
          h=int(height*detection.location_data.relative_bounding_box.height)
          w=int(height*detection.location_data.relative_bounding_box.width)
          start_point=(x-30,y-30)
          end_point=((x+w)+60,(y+h)+60)
          print(start_point,end_point,"++++++++++++++++++++++++++")
          # Blue color in BGR
          color = (255, 0, 0)

          # Line thickness of 2 px
          thickness = 1
          imgg = cv2.rectangle(imgg, start_point, end_point, color, thickness)

      #     =======================================================================
          image=imgg[ y-30:y+h+30,x-30:x+w+30]
          image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
          cv2.imwrite("sampleeee1.png",image)

          # To improve performance
          image.flags.writeable = False

          # Get the result
          results = face_mesh.process(image)

          # To improve performance
          image.flags.writeable = True

          # Convert the color space from RGB to BGR
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

          img_h, img_w, img_c = image.shape
          face_3d = []
          face_2d = []

          if results.multi_face_landmarks:
            print(len(results.multi_face_landmarks))
            jj = jj + 1
            for face_landmarks in results.multi_face_landmarks:
              print(jj, "+++++++++++++++++")
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
              # print(y)
              # See where the user's head tilting
              print("========================")
              print("========================")
              print("========================")
              print(y,x)
              print("========================")
              print("========================")
              print("========================")
              if y < -45:
                flag = 1
                count = count + 1
                text = "Looking Left"
              elif y > 5:
                flag = 1
                count = count + 1
                text = "Looking Right"
              elif x < -5:
                flag = 1
                count = count + 1
                text = "Looking Down"
              else:
                flag = 0
                count = 0
                text = "Forward"
              print(text, "======================================")
              # # Display the nose direction
              # nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
              #
              # p1 = (int(nose_2d[0]), int(nose_2d[1]))
              # p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
              #
              # cv2.line(image, p1, p2, (255, 0, 0), 2)

              # Add the text on the image
              cv2.putText(imgg, text, start_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
              if flag == 1:
                if count == 50:
                  import time

                  dt = time.strftime("%Y%m%d_%H%M%S")
                  cv2.imwrite(path + "malpractice\\" + dt + ".png", image)
                  pth = dt + ".png"
                  # insert_malpractice()
                  # requests.get("http://127.0.0.1:8000/insert_malpractice/"+ dt + ".png")
                  # db = Db()
                  # db.insert(
                  #     "insert into malpractice values(null,'1',curdate(),curtime(), '" + pth + "' )")
                  q="insert into malpractice values(null,'1',curdate(),curtime(),%s)"
                  iud(q,pth)
                  print("+_+_+_+_+_+)+)+)+)+_+_+_+_+_)()_")
                  count = 0
                  flag = 0
        except:
          pass
    #     =======================================================================



    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Detection', imgg)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()