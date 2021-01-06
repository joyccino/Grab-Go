import cv2
import numpy as np
import time
import face_recognition
import os
import os.path
#file transfer
from ftplib import FTP

def crop():
    # from cropData import cropData
    customer_name = input('Hello customer, Please enter your name.')
    # Directory 
    directory = customer_name
    # Parent Directory path 
    parent_dir = "/home/moon/Desktop/chosenones/1/customers/"
    # Path 
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path) 
    print("Directory '% s' created" % directory) 
    print("done, a directory has been generated for "+customer_name)

    print('Your webcam is getting ready...')

    # cropData()
    webcam = cv2.VideoCapture(0)
 
    if not webcam.isOpened():
        print("Could not open webcam")
        exit()
 
    sample_num = 0    
    captured_num = 0
    start_time=time.time()
    counter = 0
    grabngo = 'customer'


    
    # loop through frames
    while webcam.isOpened():
    
      # read frame from webcam 
        status, frame = webcam.read()
        sample_num = sample_num + 1

    
        if not status:
            break
 
        # display output
        cv2.imshow("captured frames", frame)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Label the results
        for (top, right, bottom, left), name in zip(face_locations, grabngo):
            if not name:
                continue

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            crop_img = frame[top:bottom, left:right]

            captured_num = captured_num + 1
            cv2.imwrite('/home/moon/Desktop/chosenones/1/customers/'+customer_name+"/"+str(captured_num)+'.jpg', crop_img)


        # press "Q" to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        end_time=time.time()
        elapsed = end_time - start_time
        if elapsed > 5:
            break
    
    # release resources
    webcam.release()
    cv2.destroyAllWindows()   

    prepath = '/home/moon/Desktop/chosenones/1/customers/'
    path = prepath+customer_name
    num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])

    if num_files < 10:
        print('Your data size is less than 10... please inform your staff.')
    else:
        print('welcome, '+customer_name+'. you are ready to go.')

    print('for file transfer')
