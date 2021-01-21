import cv2
import winsound
cam = cv2.VideoCapture(0) # 0 is for webcam. Try different numbers for different cameras attached
while cam.isOpened():
    ret, frame = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame,frame2) #difference between frames
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY) #to convert the image into greyscale
    blur = cv2.GaussianBlur(gray, (5,5), 0) #to blur the image
    _, thresh =cv2.threshold(blur, 20,255, cv2.THRESH_BINARY) #to remove the noise
    dilated = cv2.dilate(thresh,None, iterations=3) #to dilate that is opposite of threshold, to get sharper image
    contours, _ =cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #to get rectangle boxes to markout the moving things
    for c in contours:
        if cv2.contourArea(c)<4000: #smaller the value means more sensitive to movement
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3) #to draw rectangle around moving object
        winsound.Beep(500, 300) #to make beep sound when a moving object is detected
    if cv2.waitKey(10) == ord('q'): # q denotes that window can be closed by pressing key 'Q'
        break
    cv2.imshow('Camera View (press Q to exit)', frame) #to show the frame on window
