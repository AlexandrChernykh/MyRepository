import numpy as np
import cv2

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cam = cv2.VideoCapture(0)
i = 1
while i!=0:
    rv,wcImage = cam.read()
    #cv2.imshow('my webcam', wcImage)


    img = cv2.imread('in.jpg')
    #img = wcImage
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(gray, 1.211, 3)
    #faces = face_cascade.detectMultiScale(gray, 1.2, 1)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    print(len(faces))
    #cv2.imshow('img',img)
    cv2.imshow('img',cv2.flip(cv2.resize(img, (0,0), fx=0.95, fy=0.95),1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i = i -1
cv2.waitKey(0)
cv2.destroyAllWindows()
cam.release()