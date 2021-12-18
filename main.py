# This program detect move and make green rectangle around moving object
# It require to start in static environment without ane moving object. 
# Program compare video from camera with the first static frame captured from it. 

import cv2, pandas
from datetime import datetime

first_frame = None
move_status = [None, None]
date_and_time = []
df = pandas.DataFrame(columns=["Start Moving", "End Moving"])
camera = cv2.VideoCapture(0)

while True:
    is_moving = 0
    delta_frame = None
    check, frame = camera.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0 )

    if first_frame is None: 
        first_frame = gray_frame

    delta_frame = cv2.absdiff(first_frame, gray_frame)
    treshold_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    treshold_frame = cv2.dilate(treshold_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(treshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts: 
        if cv2.contourArea(contour) < 1000:
            continue
        is_moving = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    move_status.append(is_moving)
    move_status = move_status[-2:]
    
    if move_status[-1] == 1 and move_status[-2] == 0:
        date_and_time.append(datetime.now())
    if move_status[-1] == 0 and move_status[-2] == 1: 
        date_and_time.append(datetime.now())
    # print(is_moving)
    cv2.imshow("Video", frame)
    # for calibrating purposes
    # cv2.imshow("Delta", delta_frame)
    # cv2.imshow("Treshold", treshold_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        if is_moving == 1: 
            date_and_time.append(datetime.now())
        break

cv2.destroyAllWindows    
camera.release()

for i in range(0, len(date_and_time), 2):
    df = df.append({"Start Moving": date_and_time[i], "End Moving": date_and_time[i+1]}, ignore_index=True)

df.to_csv("times.csv")