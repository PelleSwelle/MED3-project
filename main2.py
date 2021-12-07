import cv2 as cv
from pynput import keyboard
from pynput.keyboard import Key, Listener

def show(key):
        print('\nYou entered {0}'.format(key))

        if key == Key.delete:
            return False


def main():
    original_image = cv.imread("reference/Wsign2.jpg")
    
    while true:
        cv.imshow("original image", original_image)



    with Listener(on_press = show) as listener:
        listener.join()

    

    

    
if __name__=="__main__":
    main()
    cv.waitKey(0)
    cv.destroyAllWindows()