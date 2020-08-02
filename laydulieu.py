import numpy as np
import os
import sqlite3
import cv2
import os.path
#--------------------------------------------------------------------
# CODE NHAP DU LIEU HINH ANH VA DAT TEN KET NOI CO SO DU LIEU
def insertOrUpdate(id, name):
    #connecting to the db
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # db_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
    conn =sqlite3.connect("./ndkm.db")
    #check if id already exists
    query = "SELECT * FROM People WHERE ID="+str(id)
    #returning the data in rows
    cursor = conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        query="UPDATE People SET Name='"+str(name)+"' WHERE ID="+str(id)
    else:
        query="INSERT INTO People(ID, Name) VALUES("+str(id)+",'"+str(name)+"')"
    conn.execute(query)
    conn.commit()
    conn.close()

face_cascade = cv2.CascadeClassifier("C:/Users/itsof/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
# insert to db
cap = cv2.VideoCapture(0)
id = input('Enter user id: ')
name = input('Enter name: ')
insertOrUpdate(id, name)
sample_number = 0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # nhận dạng khuôn mặt trên webcam
    faces = face_cascade.detectMultiScale(gray,1.3,5 )
    #vẻ hình vuông xung quanh khuôn mặt
    for (x,y,w,h) in faces:
        sample_number += 1

        if not os.path.exists('data_face'):
            os.makedirs('data_face')

        cv2.imwrite('data_face/User.'+str(id)+"."+str(sample_number)+".jpg",  gray[y:y+h,x:x+w])
        # tọa độ,tọa độ tịnh tiến,màu xanh,độ dày ò khung
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2) 

    cv2.imshow('img', img)
    cv2.waitKey(1);
    if(sample_number>100):
        break;
cap.release()
cv2.destroyAllWindows()
