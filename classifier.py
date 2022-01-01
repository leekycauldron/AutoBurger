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
    lower_black = np.array([0,0,10])
    upper_black = np.array([0,0,255])
    mask = cv2.inRange(imgHSV,lower_black,upper_black)
    
    for i in range(len(mask)): # iterate each row
        for px in range(len(mask[i])):
        
            if mask[i, px] == 255:
                    
                img[i,px] = (255,255,255) # Change pixel to white if it needs to be removed (part of mask)
    return img

def getOrderItems(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, gray) = cv2.threshold(gray, 230, 253, cv2.THRESH_BINARY)
    gray_inv = cv2.bitwise_not(gray)
    im_floodfill = gray_inv.copy()
    h, w = gray.shape[:2]
    mask = np.zeros((h+2,w+2),np.uint8)
    cv2.floodFill(im_floodfill,mask,(0,0),255)
    
    final = cv2.bitwise_xor(gray,im_floodfill)
    
    blur = cv2.GaussianBlur(final,(9,9), 0)
    imgCanny = cv2.Canny(blur, 100, 100//3)
    

    # Get number of contours (order items)
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    itm_cnt = 0
    item_coords = []
    item_corners = []
    for cnt in contours:
   
        x, y, w, h = cv2.boundingRect(cnt)

        # Get corners in item (used to classify order item)
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*peri,True)
        objCorners = len(approx)
        item_corners.append(objCorners)


        itm_cnt += 1
        item_coords.append([(x,x+w),(y,y+h)])

        """cv2.drawContours(img, cnt, -1, (0, 0, 0), 3)
            
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)"""
                        
    cv2.imshow('img',img)
    cv2.imshow('greyinv',gray_inv)
    cv2.imshow('fillog',im_floodfill)
    
    cv2.imshow("fill",final)
    cv2.imshow('blur',blur)
    cv2.imshow('canny',imgCanny)

    cv2.waitKey(5)

    return itm_cnt, item_coords, item_corners


def classifyShape(sides,classify):
    if classify == "side":
        if sides <= 6:
            return "cola"
        else:
            return "fries"
    elif classify == "burger":
        return "burger"