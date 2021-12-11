import cv2

camera = cv2.VideoCapture(0)
while True:
    check, frame = camera.read()
    cv2.imshow("Captured video", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows    
camera.release()