import numpy as np
import os
import pickle, sqlite3
import cv2
from PIL import Image
import speech_recognition
import pyttsx3
# import app
#--------------------------------------------------------------------
# CODE KET NOI DU LIEU NHAN DIEN HINH ANH KHUON MAT
# thư viện nhận dạng khuôn mặt ở đâu trên camera
face_cascade = cv2.CascadeClassifier('C:/Users/itsof/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
# thư viện nhận dạng đó là ai
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./trainer/huanluyen.yml")
name=''

def getProfile(Id):
    conn=sqlite3.connect("./ndkm.db")
    query="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(query)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

#cap = cv2.VideoCapture("rtsp://admin:admin@172.16.1.45:554/cam/realmonitor?channel=1&subtype=1&unicast=true&proto=Onvif")
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
def main():
    while True:
    #comment the next line and make sure the image being read is names img when using imread
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50:
                profile=getProfile(id)
                if profile != None:
                    cv2.putText(img, ""+str(profile[1]), (x+10, y+h+30), font, 1, (0,255,0), 1);
                    name = str(profile[1])
            else:
                cv2.putText(img, "Unknown", (x, y + h + 30), font, 0.4, (0, 0, 255), 1);
                name = "unknown"


        cv2.imshow('img', img)

        if(cv2.waitKey(1) == ord('q')):
            # print(name)
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return name
main()



