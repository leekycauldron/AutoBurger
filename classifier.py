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
    imgCanny = cv2.Canny(blur, 300, 300//3)
    

    # Get number of contours (order items)
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    itm_cnt = 0
    item_coords = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print("AREA: " + str(area))
        x, y, w, h = cv2.boundingRect(cnt)
        #print("ACTUAL:" + str((x+w)*(y+h)))
        #if area >= 13.5 and (x+w)*(y+h) >= 8000: # Parts of food accidentally detected sometimes.
        if True:
            
           
            if len(item_coords) != 0:
                for coord in range(len(item_coords)):
                    if abs(item_coords[coord][0][0] - x) < 50: # Check if the box is inside another box
                        
                        print("{} is less than {}".format(x,item_coords[coord][0][0]))
                        # Sometimes false positive contours are added before real contours
                        # To prevent this, checking the shape area will allow me to find the right contour.
                        if (x+w)*(y+h) > item_coords[coord][0][1] * item_coords[coord][1][1]: 
                            
                            print("Removing detected false positive... {} is bigger than {}".format((x+w)*(y+h),item_coords[coord][0][1] * item_coords[coord][1][1]))
                            
            
                            cv2.rectangle(img, (item_coords[coord][0][0], item_coords[coord][0][1]),(item_coords[coord][1][0], item_coords[coord][1][1]), (0,0,255), 2)

                            item_coords.pop(coord) # The previously added contour was the imposter (sus).
                            # Dont add another count to itm_cnt since net gain is 0 (-1 then +1).
                            item_coords.append([(x,x+w),(y,y+h),area])
                            cv2.drawContours(img, cnt, -1, (0, 0, 0), 3)
                
                            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)


                        cv2.drawContours(img, cnt, -1, (0, 0, 0), 3)
            
                        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
                        break 
                    else:
                        print("OK {} is greater than {}".format(x,item_coords[coord][0][0]))
                        print(x,item_coords[coord][0][0])
                        itm_cnt += 1
                        item_coords.append([(x,x+w),(y,y+h),area])
                        cv2.drawContours(img, cnt, -1, (0, 0, 0), 3)
            
                        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                        
            else:
                print("COORDS LIST IS EMPTY, ADDING FIRST VALUE...")
                itm_cnt += 1
                item_coords.append([(x,x+w),(y,y+h),area])
                cv2.drawContours(img, cnt, -1, (0, 0, 0), 3)
            
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

    while itm_cnt > 3: #TEMPORARY. THERE SHOULD NEVER BE MORE THAN THREE ORDERS.
        itm_cnt -= 1
        item_coords.pop(-1)
    cv2.imshow('img',img)
    cv2.imshow('greyinv',gray_inv)
    cv2.imshow('fillog',im_floodfill)
    
    cv2.imshow("fill",final)
    cv2.imshow('blur',blur)
    cv2.imshow('canny',imgCanny)
    #cv2.imshow('bw',blackAndWhiteImage)
    cv2.waitKey(5)

    return itm_cnt, item_coords

def getDomColor(img, coords):
    colors = []
    tmp_img = img[coords[0][1]:coords[1][1], coords[0][0]:coords[1][0]]
    
    for i in range(coords[0][1]-coords[0][0]): # loop each row of pixels. 
        for j in range(coords[1][1]-coords[1][0]): # loop each pixel in row
            (b,g,r) = tmp_img[j,i]
            
            colors.append((b,g,r))

    return colors