import time
import cv2
import mss
import coord
from direct_input import W,A,S,D,PressKey,ReleaseKey
import numpy as np
from PIL import ImageGrab
import cv2
from alexnet import alexnet
from getkeys import key_check

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'pygta5-car-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2',EPOCHS)
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)
def accelerate():
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    PressKey(W)
def left():
    ReleaseKey(S)
    ReleaseKey(D)
    PressKey(W)
    PressKey(A)
def right():
    ReleaseKey(A)
    ReleaseKey(S)
    PressKey(D)
    PressKey(W)
def neutral():
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    ReleaseKey(W)
def deaccelerate():
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(W)
    PressKey(S)

for i in range(4):
    print(4-i)
    time.sleep(1)
    
def proccess_frame(original_frame):
    dim = (800,600)  # resize image (height, width)
    frame = cv2.resize(original_frame, dim, interpolation = cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    frame = cv2.resize(frame, (80,60)) #for model
    return frame


paused = False
while True:
    # Part of the screen to capture
    # 800x600 windowed mode
    
    if not paused:
        try:
            l,t,w,h = coord.coord() # of window of GTAV
        except:
            l,t=0,0
            w,h=800,600
        size = {"top": t, "left": l, "width": 800, "height": 600}
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array
        sct=mss.mss()
        original_frame = np.array(sct.grab(size)) # has width*height*4 elements (4 for RGBA)
        frame=proccess_frame(original_frame)
        moves = list(np.around(model.predict([frame.reshape(80,60,1)])[0]))
        print(moves)
        if moves == [1,0,0]:
            left()
        elif moves == [0,1,0]:
            accelerate()
        elif moves == [0,0,1]:
            right()
        #print(frame)
        #print(frame.shape)
        
        cv2.imshow("myGAME", frame)
        
        '''
        #to Display the picture in grayscale
        cv2.imshow('OpenCV/Numpy grayscale',cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY))
        '''
        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
                paused = True
                neutral()
                time.sleep(1)
                
        print("fps: {}".format(1 / (time.time() - last_time)))
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
                
    keys = key_check()
    if 'T' in keys:
        if paused:
            paused = False
            time.sleep(1)
                
       