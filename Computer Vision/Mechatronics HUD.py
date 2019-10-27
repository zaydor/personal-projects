######################
# Author: Isaiah Dorado
# Email: isaiahdorado@gmail.com
# Date: 9/25/19
# 
# With help from OpenCV Documentation, StackOverFlow,
# and https://thecodacus.com/opencv-object-tracking-colour-detection-python/
#
# Project Title: 'Cyclops: The Mechatronics Software Recruit Project'
# 
# Psuedocode: 
# On start, this program opens a window and connects to a webcam. 
# It then takes a live feed from the webcam and displays it in the created window with a Heads Up Display.
# With the live feed and a given user color to detect, the program identifies the user color in the window.
# This satisfies the Level 1 Deliverable.
# 
# Then the program finds the location of the colored object, 
# determines its location on the screen in pixels, and highlights its location on screen.
# This satisfies Level 2 Deliverable.
#
# Then there is a real time indicator that tells the user where to point the camera to center the object in frame.
# The program also has its own frame rate tester that prints to console the frame rate for testing purposes.
# This satisfies Level 3 Deliverable.
#
# For a more personal touch, I added a simple menu to tell the user what buttons to press to change HUD color and
# what color the program searches for (currently just green and orange).
######################

import numpy as np
import cv2
import keyboard
import time

vc = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX # Initiaize font

##### Initialize HUD color (Inital Light Blue)
B = 250
G = 250
R = 13

##### Initialize Upper and Lower Bounds for object detection (Initial to find orange)
objUpB = 15
objLowB = 5

objUpG = 255
objLowG = 100

objUpR = 255
objLowR = 255

btmY = 460
LftX = 10
topY = 20

if vc.isOpened(): # Get first frame when program starts
    rolling, frame = vc.read()
    
else:
    rolling = False


while rolling: # Camera feed loop

    ### Menu stuff
    if not keyboard.is_pressed('m'):
        cv2.putText(frame,'Menu: Hold M Key',(LftX,btmY), font, 0.5,(255,255,255),1,cv2.LINE_AA)

    ### Display the menu
    if keyboard.is_pressed('m'):
        cv2.rectangle(frame,(120,360),(520,430),(0,0,0),-1)
        cv2.putText(frame,'Press A to ID Orange     Press S to ID Green',(122,382), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(frame,'Press 1 for Blue HUD     Press 2 for Red HUD',(122,412), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        
    if keyboard.is_pressed('1'): # Change HUD color to Light Blue
        B= 250
        G= 250
        R= 13
    elif keyboard.is_pressed('2'): # Change HUD color to Red
        B= 25
        G= 25
        R= 210
        
    elif keyboard.is_pressed('3'): # Change HUD color to Green            For menu formatting sake, this HUD color is an easter egg :)
        B= 33          
        G= 255
        R= 17

    if keyboard.is_pressed('a'): # Camera detects Orange
        objUpB = 15
        objLowB = 5

        objUpG = 255
        objLowG = 100

        objUpR = 255
        objLowR = 255
        
    if keyboard.is_pressed('s'): # Camera detects Green
        objUpB = 70
        objLowB = 36

        objUpG = 255
        objLowG = 25

        objUpR = 255
        objLowR = 25

    if keyboard.is_pressed('p'): # For tesing frame rate (from: https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/ )
        num_frames = 120;
     
        print ("Capturing {0} frames".format(num_frames))
 
        # Start time
        start = time.time()
     
        # Grab a few frames
        for i in range(0, num_frames) :
            rolling, frame = vc.read()
 
     
        # End time
        end = time.time()
 
        # Time elapsed
        seconds = end - start
        print ("Time taken : {0} seconds".format(seconds))
 
        # Calculate frames per second
        fps  = num_frames / seconds;
        print ("Estimated frames per second : {0}".format(fps))
        
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert camera feed pixels from BGR to HSV
    lower_bound = np.array([objLowB,objLowG,objLowR], np.uint8) # Initialize upper and lower bound for color detection
    upper_bound = np.array([objUpB,objUpG,objUpR], np.uint8)

    mask = cv2.inRange(hsv, lower_bound, upper_bound) # Create mask that only displays color in our given range

    # Creating arrays
    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))

    maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen) # Reduce some noise
    maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose) # Reduce more noise
    maskFinal = maskClose
    
    ### Highlight object on main camera using noise reduced image for more accuracy
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 
    cv2.drawContours(frame,conts,-1,(255,0,0),3)

    for i in range(len(conts)): # loop while specified color is on screen
        x,y,w,h=cv2.boundingRect(conts[i]) # identify where object is in pixels
        ### Tells user where to move camera in order to center the object
        if(y > 280 and x > 340):
            cv2.putText(frame,'Lower Right',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        if(y < 200 and x > 340):
            cv2.putText(frame,'Upper Right',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        if(y > 200 and y < 280 and x > 340):
            cv2.putText(frame,'Right',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)

        if(y > 280 and x < 260):
            cv2.putText(frame,'Lower Left',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        if(y < 200 and x < 260):
            cv2.putText(frame,'Upper Left',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        if(y > 200 and y < 260 and x < 260):
            cv2.putText(frame,'Left',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)

        if(y > 200 and y < 280 and x > 260 and x < 340 ):
            cv2.putText(frame,'Centered',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)

        if(y > 280 and x < 340 and x > 260):
           cv2.putText(frame,'Down',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)

        if(y < 200 and x < 340 and x > 260):  
            cv2.putText(frame,'Up',(LftX,topY), font, 0.5,(255,255,255),1,cv2.LINE_AA)

    ### Build HUD
    cv2.ellipse(frame,(320,240),(120,120), 0, -30, 30, (B,G,R), 2)
    cv2.ellipse(frame,(320,240),(120,120), 0, 150, 210, (B,G,R), 2)        
    cv2.rectangle(frame,(0,0),(640,480),(0,0,0),8)
    cv2.circle(frame,(320,240), 63, (B,G,R), 2)
    cv2.line(frame,(305,240),(335,240),(B,G,R),2)
    cv2.line(frame,(320,225),(320,255),(B,G,R),2)
    cv2.line(frame,(320,318),(320,303),(B,G,R),2)
    cv2.line(frame,(320,240-63),(320,240-75),(B,G,R),2)
    cv2.line(frame,(320-63,240),(320-75,240),(B,G,R),2)
    cv2.line(frame,(320+63,240),(320+75,240),(B,G,R),2)

    cv2.line(frame,(40,40),(40,440),(B,G,R),2)
    cv2.line(frame,(600,40),(600,440),(B,G,R),2)
    cv2.line(frame,(40,40),(65,40),(B,G,R),2)
    cv2.line(frame,(40,440),(65,440),(B,G,R),2)
    cv2.line(frame,(600,40),(575,40),(B,G,R),2)
    cv2.line(frame,(600,440),(575,440),(B,G,R),2)
    ### End HUD Build

    cv2.imshow("Camera Feed", frame)
    rolling, frame = vc.read()
    key = cv2.waitKey(10)
    
    if key == 27: # Exit loop when ESC is pressed
        break

cv2.destroyAllWindows()
