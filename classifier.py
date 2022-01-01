import cv2, os
from PIL import ImageGrab
import numpy as np

def getOrderImg(order_region):
    # Get the customer's order and return the image of it.
    img = ImageGrab.grab(order_region)
    img.save(os.path.join("tmp","order.jpg"))
    img.close()

    img = cv2.imread(os.path.join("tmp","order.jpg"))
    os.remove(os.path.join("tmp","order.jpg"))
    return img

def removeText(img): # Get rid of the plus sign (if any)

    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_black = np.array([0,0,13])
    upper_black = np.array([0,0,240])
    mask = cv2.inRange(imgHSV,lower_black,upper_black)

    for i in range(len(mask)): # iterate each row
        for px in range(len(mask[i])):
        
            if mask[i, px] == 255:
                    
                img[i,px] = (255,255,255) # Change pixel to white if it needs to be removed (part of mask)
    return img

def getOrderItems(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(gray, 400, 400//3)

    # Get number of contours (order items)
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    itm_cnt = 0
    item_coords = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if area >= 13 and (x+w)*(y+h) >= 8000: # Parts of food accidentally detected sometimes.
            itm_cnt += 1
            item_coords.append([(x,y),(x+w,y+h)])

    return itm_cnt, item_coords