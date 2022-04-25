# This program detect move and make green rectangle around moving object
# It require to start in static environment without ane moving object. 
# Program compare video from camera with the first static frame captured from it. 

import cv2
import datetime as dt
import pandas as pd
import os
import constant

first_frame = None
camera = cv2.VideoCapture(0)
move_started = False
detect_move = False

"""
Save date and time of start and stop moving to csv file
"""
def save_datetime(mode):
    date_time = dt.datetime.now()
    print(date_time)
    
    if not os.path.isfile("show_time.csv"):
        f = open("show_time.csv", "a")
        f.write("Move started,Move stoped")
        f.close()

    df = pd.read_csv("show_time.csv")

    match mode:
        case constant.START_MOVE:
            df = df.append({"Move started" : date_time}, ignore_index = True)
            df.to_csv("show_time.csv", index = False)

        case constant.STOP_MOVE:
            df.iloc[len(df) - 1, 1] = date_time
            df.to_csv("show_time.csv", index = False)

while True:
    delta_frame = None
    check, frame = camera.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0 )
    detect_move = False

    if first_frame is None: 
        first_frame = gray_frame

    delta_frame = cv2.absdiff(first_frame, gray_frame)
    treshold_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    treshold_frame = cv2.dilate(treshold_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(treshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts: 
        if cv2.contourArea(contour) < 1000:
            continue
        else: 
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            if move_started == False:
                move_started = True
                print("Move started")
                save_datetime(constant.START_MOVE)
            detect_move = True
        
    if move_started == True and detect_move == False:
            move_started = False
            print("Move stoped")
            save_datetime(constant.STOP_MOVE)

    cv2.imshow("Video", frame)
    # for calibrating purposes
    # cv2.imshow("Delta", delta_frame)
    # cv2.imshow("Treshold", treshold_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows    
camera.release()