# This program detect move and make green rectangle around moving object
# It require to start in static envernoment without ane moving object. 
# Program compare video from camera with the first static frame captured from it. 

import cv2

first_frame = None
camera = cv2.VideoCapture(0)

while True:
    delta_frame = None
    check, frame = camera.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0 ) # get more knowlege about this concept

    if first_frame is None: 
        first_frame = gray_frame
        # in lecture there is ***continue*** here; I don't know why exactly because in my opinion program will be work correctly

    delta_frame = cv2.absdiff(first_frame, gray_frame)
    treshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    treshold_frame = cv2.dilate(treshold_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(treshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts: 
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows    
camera.release()