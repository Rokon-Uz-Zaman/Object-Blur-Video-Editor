

#Blur Object in a video
# A.B.M. Rokon-Uz-Zaman Roman


''''
imutils	0.5.4
numpy	1.21.3
opencv-contrib-python	4.5.4.58
pip	9.0.1
setuptools	28.8.0
'''

import cv2  #opencv contrib
import imutils

import tkinter as tk
from tkinter import filedialog


#filepath='test.mp4' #work
#filepath='C:/Users/Roman/PycharmProjects/R_video player working/3.mp4' #work

def trackingfun(path):
    cap = cv2.VideoCapture(path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))
    size = (frameWidth, frameHeight)
    # result = cv2.VideoWriter('filename.avi',cv2.VideoWriter_fourcc(*'MJPG'),10,size)
    #out = cv2.VideoWriter('outputFile.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
    out = cv2.VideoWriter('outputFile.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, size)


    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=720)
        frame=cv2.putText(frame,'Press S to select',(20,100),font ,2,(0,0,255))
        #cv2.waitKey(10)
        cv2.imshow('press S to select', frame)


        if cv2.waitKey(40) & 0xff == ord('s'):
            bb = cv2.selectROI(frame, False)
            cv2.destroyAllWindows()
            break

    # create tracker obj
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bb)

    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))
    size = (frameWidth, frameHeight)
    # result = cv2.VideoWriter('filename.avi',cv2.VideoWriter_fourcc(*'MJPG'),10,size)
    # out = cv2.VideoWriter('outputFile.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
    out = cv2.VideoWriter('outputFile.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, size)

    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=720)
        trackCheck, bb = tracker.update(frame)
        if trackCheck:
            topLeft = (int(bb[0]), int(bb[1]))
            bottomRight = (int(bb[0] + bb[2]), int(bb[1] + bb[3]))
            #cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 0), 5)

            print(topLeft,bottomRight)
            h,w=frame.shape[:2]
            kernel_height=(w//7) | 1
            kernel_width=(w//7) | 1

            start_y=int(bb[1])
            end_y=int(bb[1] + bb[3])
            start_x=int(bb[0])
            end_x=int(bb[0] + bb[2])
            cropped=frame[start_y:end_y,start_x: end_x]
            #cropped  = frame[38: 75, 330: 370]
            blured= cv2.GaussianBlur(cropped,(kernel_width,kernel_height),0)
            frame[start_y: end_y, start_x: end_x] = blured



        cv2.imshow('Blured the selected object', frame)
        out.write(frame)





        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


#trackingfun(filepath)
#print(filepath)  #test


###################   GUI section

root = tk.Tk("Object Tracking With GUI","Object Tracking With GUI")
root.geometry("400x300")  # window size

label1 = tk.Label(root, text='Object Blur   ', width=40)
label1.grid(row=1, column=1)

button1 = tk.Button(root, text='Select a file video file ', width=30, command=lambda: fileUpload())
button1.grid(row=2, column=1)


label37 = tk.Label(root, text='                   ', width=40)
label37.grid(row=3, column=1)
label35 = tk.Label(root, text='                        ', width=40)
label35.grid(row=4, column=1)
label3 = tk.Label(root, text='Press S to Select then Press enter  ', width=40)
label3.grid(row=6, column=1)
label2 = tk.Label(root, text='Press Q to Quit video  ', width=40)
label2.grid(row=7, column=1)




def fileUpload():
    uploaded = filedialog.askopenfilename()
    #img = cv2.imread(uploaded, 0)
    #trackf()
    print(uploaded)
    trackingfun(uploaded)

    print("file path seleted success")
    #cv2.imshow('blank and white image', img)




root.mainloop()


#######    GUI section end





