import numpy as np
import cv2
import time
from getkeys import key_check
import os
import coord
import mss

def proccess_frame(original_frame):
    dim = (80,60)  # resize image (height, width)
    frame = cv2.resize(original_frame, dim)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    frame=np.reshape(frame, (1,4800))
    frame=frame[0]
    return frame

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''
    output = [0,0,0]
    
    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    elif 'W' in keys:
        output[1] = 1
    return output

file_x = 'training_data_x.npy'
if os.path.isfile(file_x):
    print('File exists, loading previous data!')
    try:
        training_data_x = list(np.load(file_x))
    except:
        print('no data in file, starting fresh!')
        training_data_x = []
else:
    print('File does not exist, starting fresh!')
    training_data_x = []
    
file_y = 'training_data_y.npy'
if os.path.isfile(file_y):
    print('File exists, loading previous data!')
    try:
        training_data_y = list(np.load(file_y))
    except:
        print('no data in file, starting fresh!')
        training_data_y = []
else:
    print('File does not exist, starting fresh!')
    training_data_y = []



def main():

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
        
    while(True):
        # 800x600 windowed mode
        try:
            l,t,w,h = coord.coord()
        except:
            l,t=0,0
            w,h=800,600
        size = {"top": t, "left": l, "width": 800, "height": 600}
        last_time = time.time()
        sct=mss.mss()
        original_frame = np.array(sct.grab(size)) # has width*height*4 elements (4 for RGBA)
        screen=proccess_frame(original_frame)
        keys = key_check()  
        
        if 'T' in keys:
            cv2.destroyAllWindows()
            break
        
        output = np.array(keys_to_output(keys))
        
        #training_data.append([screen,output])
        #print(screen)
        #print(output)
        training_data_x.append(screen)
        training_data_y.append(output)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
        if len(training_data_x) % 500 == 0:
            print(len(training_data_x))
            print(len(training_data_y))
            np.save(file_x,training_data_x)
            np.save(file_y,training_data_y)
            
main()