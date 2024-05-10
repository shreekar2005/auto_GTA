import time
import cv2
import mss
import numpy
import coord
from direct_input import W,A,S,D,PressKey,ReleaseKey

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
    return frame


while True:
    # Part of the screen to capture
    # 800x600 windowed mode
    try:
        l,t,w,h = coord.coord() # of window of GTAV
    except:
        l,t=0,0
        w,h=800,600
    size = {"top": t, "left": l, "width": 800, "height": 600}
    last_time = time.time()
    # Get raw pixels from the screen, save it to a Numpy array
    sct=mss.mss()
    original_frame = numpy.array(sct.grab(size)) # has width*height*4 elements (4 for RGBA)
    frame=proccess_frame(original_frame)
    print(frame)
    print(frame.shape)
    
    cv2.imshow("myGAME", frame)
    
    '''
    #to Display the picture in grayscale
    cv2.imshow('OpenCV/Numpy grayscale',cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY))
    '''
    
    print("fps: {}".format(1 / (time.time() - last_time)))
    # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break