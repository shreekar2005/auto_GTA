# this to get the coordinates of the game window
import pyscreenshot as ImageGrab
import pygetwindow as gw

def coord():
    window = gw.getWindowsWithTitle("Grand Theft Auto V")[0]
    x1, y1, x2, y2 = window.left, window.top, window.left + window.width, window.top + window.height
    x1+=8
    y1+=35
    x2-=8
    y2-=5
    return x1,y1,x2-x1,y2-y1

if __name__ == "__main__":
    print("x,y,width,height = ",coord())
