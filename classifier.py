import cv2, os
from PIL import ImageGrab, Image
import numpy as np
import matplotlib.pyplot as plt

def getOrderImg(order_region):
    # Get the customer's order and return the image of it.
    img = ImageGrab.grab(order_region)
    img.save(os.path.join("tmp","orders.jpg"))
    img.close()

    img = cv2.imread(os.path.join("tmp","orders.jpg"))
    
    return img

def removeText(img): # Get rid of the plus sign (if any)

    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_black = np.array([0,0,3]) # OG: 10
    upper_black = np.array([0,0,255]) # OG: 250
    mask = cv2.inRange(imgHSV,lower_black,upper_black)
    
    for i in range(len(mask)): # iterate each row
        for px in range(len(mask[i])):
        
            if mask[i, px] == 255:
                    
                img[i,px] = (255,255,255) # Change pixel to white if it needs to be removed (part of mask)
    return img

def getOrderItems(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, gray) = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    gray_inv = cv2.bitwise_not(gray)
    im_floodfill = gray_inv.copy()
    h, w = gray.shape[:2]
    mask = np.zeros((h+2,w+2),np.uint8)
    cv2.floodFill(im_floodfill,mask,(0,0),255)
    
    final = cv2.bitwise_xor(gray,im_floodfill)
    
    dil = cv2.dilate(final,(7,7),iterations=1)
    imgCanny = cv2.Canny(dil, 500, 500//3)
    
    # Get number of contours (order items)
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    itm_cnt = 0
    item_coords = []
   
    for cnt in contours:
   
        x, y, w, h = cv2.boundingRect(cnt)

        # Get corners in item (used to classify order item)
        """ peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*peri,True)
        objCorners = len(approx)
        item_corners.append(objCorners)""" # This is deprecated.

        itm_cnt += 1
        item_coords.append([(x,x+w),(y,y+h)])
    """                
    cv2.imshow('img',img)
    cv2.imshow('greyinv',gray_inv)
    cv2.imshow('fillog',im_floodfill)
    cv2.imshow('dilate',dil)
    cv2.imshow("fill",final)
    cv2.imshow('blur',blur)
    cv2.imshow('canny',imgCanny)

    cv2.waitKey(1)""" # Uncomment this block to show the images being processed.

    return itm_cnt, item_coords


def classifyShape(_class,coords):
    if _class == "side":
        img = cv2.imread(os.path.join("tmp","orders.jpg"))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = img[coords[1][0]:coords[1][1],coords[0][0]:coords[0][1]]
        if img.shape[0] * img.shape[1] <= 500: # False positive, discard.
            return "fpos"
       
        #plt.imshow(img, interpolation='none')
        #plt.show() # UNCOMMENT this block to show the image on a graph (this operation is blocking).

        colors = []
 
        for i in range(img.shape[0]): # loop each row of pixels. 
            for j in range(img.shape[1]): # loop each pixel in row
                colors.append(img[i,j])

        r_sum = 0
        g_sum = 0
        b_sum = 0
        for color in colors:
            r_sum += color[0]
            g_sum += color[1]
            b_sum += color[2]
        prod = img.shape[0] * img.shape[1]
        avg_color = [r_sum//prod,g_sum//prod,b_sum//prod]

        if avg_color[2] > avg_color[0] and avg_color[2] > avg_color[1]:
            return "fries"
        else:
            return "cola"

    elif _class == "main":
        # Use color detetion
        img = cv2.imread(os.path.join("tmp","orders.jpg"))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = img[coords[1][0]:coords[1][1],coords[0][0]:coords[0][1]]
        if img.shape[0] * img.shape[1] <= 500: # False positive, discard.
            return "fpos"
       
        #plt.imshow(img, interpolation='none')
        #plt.show() # UNCOMMENT this block to show the image on a graph (this operation is blocking).
        try:
            r1,g1,b1 = img[img.shape[0]- 26,img.shape[1] - 9] # This will allow the color to be detected no matter the player perpective.
            r2,g2,b2 = img[img.shape[0]- 26,img.shape[1] - 5]
        except: return "fpos"
        sum1 = int(r1) + int(g1) + int(b1)
        sum2 = int(r2) + int(g2) + int(b2)
        
        avg = (sum1 + sum2) // 2

        colors = []

        for i in range(img.shape[0]): # loop each row of pixels. 
            for j in range(img.shape[1]): # loop each pixel in row
                colors.append(img[i,j])


        r_sum = 0
        g_sum = 0
        b_sum = 0
        for color in colors:
            r_sum += color[0]
            g_sum += color[1]
            b_sum += color[2]
        prod = img.shape[0] * img.shape[1]
        avg_color = [r_sum//prod,g_sum//prod,b_sum//prod]

        
        if 200 < avg_color[0] and 185 < avg_color[1]:
            return "burger3"

        if avg >= 100 and avg <= 300: # Should detect the meat in the burger
            return "burger1"
        else:
            return "burger2"
