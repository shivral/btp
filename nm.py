import cv2
import imutils
import numpy as np
import argparse


import cv2
import numpy as np
import dlib

def fd(inputpath,outputpath,ar):
    detector = dlib.get_frontal_face_detector() #hog linear svm
    frame=cv2.imread(inputpath)
    
    # frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    i = 0
    for face in faces:

        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        i = i+1
        id,ind = findNearest(ar, 200, x, y)
        if id !=-1:
            ar.pop(id)

        cv2.putText(frame, 'face num #'+str(ind), (x-10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        print(face, i)
    cv2.imwrite(outputpath, frame)

def findNearest(cord,delta,x,y):
    delta=120
    for id,(a,b,ind) in enumerate(cord):
        if abs(x-a)<=delta and abs(y-b)<=delta:
            return  id,ind
    return (-1,-1)

def fd3(inputpath,outputpath,ar):


    detector = dlib.get_frontal_face_detector() #har cascade
    frame=cv2.imread(inputpath)
    # frame = cv2.flip(frame, 1)
    faceCascade = cv2.CascadeClassifier("cascade.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    i = 0
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        # X = (x +
        # Y = (y + h) // 2
        # ind=findNearest(ar,150,x,y)
        id,ind = findNearest(ar, 200, x, y)
        if id !=-1:
            ar.pop(id)

        # print(ar[ind],x,y)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, 'face num' + str(x) + "#" + str(y)+"#"+str(ind), (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imwrite(outputpath, frame)


def fd2(inputpath,outputpath):


    detector=dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")
    frame=cv2.imread(inputpath)

    # frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(image_rgb)

    i = 0
    print(faces)
    for face in faces:
        print("face ",face)

        x, y = face.rect.left(), face.rect.top()
        x1, y1 = face.rect.right(), face.rect.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        i = i+1



        print(face, i)
    cv2.imwrite(outputpath, frame)

import os
from mtcnn import MTCNN
import cv2
def detect(inputpath,outputpath) :
    pixels = cv2.imread(inputpath)

    detector = MTCNN(min_face_size=40, scale_factor=0.9, steps_threshold=[0.9, 0.9, 0.9])
    faces = detector.detect_faces(pixels)
    cnt=0
    for face in faces:
        x, y, width, height = face['box']
        cv2.rectangle(pixels, (x, y), (x+width, y+height), (0, 255, 0), 2)
        face_coordinates = (x, y, x+width, y+height)
        cnt+=1
        print(face_coordinates, cnt)
    cv2.imwrite(outputpath, pixels)
import  os
def mark(crd,imgpth,outpth):
    frame=cv2.imread(imgpth)
    for x,y,ind in crd:
        cv2.rectangle(frame, (x, y), (x + 100, y + 100), (0, 255, 0), 2)
        cv2.putText(frame, 'face num' + str(x) + "#" + str(y), (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imwrite(outpth,frame)
if __name__ == "__main__":
    directory = 'Photo data 2'
    cnt=0
    stg= {18, 11, 22, 19}
    ar=[]
    cord=open("cordinates.txt","r")
    ar=[]
    ind=0
    for i in cord:
        x,y=map(int,i.strip().split())
        ar.append((x,y,ind))
        ind+=1
    for i in range(len(ar)):
        print(i,ar[i])
    # print(*ar,sep="\n")

    # fd3('Photo data 2\IMG20230120140026.jpg',str("harcas\\"+"res.png"),ar)
    fd3('Photo data 2\IMG20230120140026.jpg',str("Cord\\"+"reshar.png"),ar.copy())
    mark(ar.copy(),'Photo data 2\IMG20230120140026.jpg',str("Cord\\"+"resCords.png"))

    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
        # checking if it is a file
        # if os.path.isfile(f):
            # if cnt==15:
            # if cnt in stg:
            #

            # fd3(str(f), str("harcs\\" + filename), ar)
            # detect(str(f), str("mtcnn\\" + filename))
            # detectByPathImage(str(f),"Photo_out2\imgpp"+str(cnt)+".jpg")
            #
            # cnt+=1
            # print(f)
