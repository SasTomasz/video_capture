import cv2

first_frame = None

camera = cv2.VideoCapture(0)
while True:
    check, frame = camera.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if first_frame is None: 
        first_frame = gray_frame

    cv2.imshow("Captured video", gray_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows    
camera.release()