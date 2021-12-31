import pyautogui
import cv2
import numpy as np
import os
from PIL import ImageGrab

textBubble1 = textBubble2 = burger1 = burger2 = burger3 = fries =  cola = done1 = None


if __name__ == "__main__":
    print("AutoBurger v1")
    print("For best results please move your camera angle to match the one in the image (camera_angle.jpg).")
    print("Follow the instructions and click enter when finished with each instruction.\n\n")
    

    #Get the needed coordinates on the users screen.
    input("Please move your cursor to the top left of the customer speech bubble then press the ENTER key.")
    textBubble1 = pyautogui.position()
    input("Please move your cursor to the bottom right of the customer speech bubble then press the ENTER key.")
    textBubble2 = pyautogui.position()
    input("Please move your cursor to the middle of the first burger (top left burger on menu) then press the ENTER key.")
    burger1 = pyautogui.position()
    input("Please move your cursor to the middle of the second burger (top right burger on menu) then press the ENTER key.")
    burger2 = pyautogui.position()
    input("Please move your cursor to the middle of the third burger (burger on second row on menu) then press the ENTER key.")
    burger3 = pyautogui.position()
    input("Please move your cursor to the middle of the fries on the menu then press the ENTER key.")
    fries = pyautogui.position()
    input("Please move your cursor to the middle of the cola on the menu then press the ENTER key.")
    cola = pyautogui.position()
    input("Please move your cursor to the top left of the done button on the menu then press the ENTER key.")
    done1 = pyautogui.position()
    
    

    #Take screenshots of food items and done button. This only needs to run on the first time or if the images are removed (either by user or program).
    if not os.path.isfile(os.path.join("images","burger1.jpg")): 
        burger1region = (burger1[0]-32,burger1[1]-32,burger1[0]+32,burger1[1]+32)
        img = ImageGrab.grab(burger1region)
        img.save(os.path.join("images", "burger1.jpg"))
        img.close()
    if not os.path.isfile(os.path.join("images","burger2.jpg")): 
        burger2region = (burger2[0]-32,burger2[1]-32,burger2[0]+32,burger2[1]+32)
        img = ImageGrab.grab(burger2region)
        img.save(os.path.join("images", "burger2.jpg"))
        img.close()

    if not os.path.isfile(os.path.join("images","burger3.jpg")): 
        burger3region = (burger3[0]-32,burger3[1]-32,burger3[0]+32,burger3[1]+32)
        img = ImageGrab.grab(burger3region)
        img.save(os.path.join("images", "burger3.jpg"))
        img.close()

    if not os.path.isfile(os.path.join("images","fries.jpg")): 
        friesregion = (fries[0]-32,fries[1]-32,fries[0]+32,fries[1]+32)
        img = ImageGrab.grab(friesregion)
        img.save(os.path.join("images", "fries.jpg"))
        img.close()
    
    if not os.path.isfile(os.path.join("images","cola.jpg")): 
        colaregion = (cola[0]-32,cola[1]-32,cola[0]+32,cola[1]+32)
        img = ImageGrab.grab(colaregion)
        img.save(os.path.join("images", "cola.jpg"))
        img.close()
    
    # Get text bubble image
    textBubbleregion = (textBubble1[0],textBubble1[1],textBubble2[0],textBubble2[1])
    img = ImageGrab.grab(textBubbleregion)

    img.save(os.path.join("tmp","textbubble.jpg"))
    img.close()
    img = cv2.imread(os.path.join("tmp","textbubble.jpg"))
    os.remove(os.path.join("tmp","textbubble.jpg"))
    final = img.copy()

    # Filter out all text.
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_black = np.array([0,0,25])
    upper_black = np.array([0,0,179])
    mask = cv2.inRange(imgHSV,lower_black,upper_black)
    res = cv2.bitwise_and(img,img,mask=mask)
    for i in range(len(mask)): # iterate each row
        for px in range(len(mask[i])):
            if px == 1:
                #print(final[i][px])
                print('yes')
                final[i,px] = [255,0,0] # Change pixel to white is it needs to be removed (part of mask)
    cv2.imshow("img", img)
    print(img)
    cv2.imshow("mask",mask)
    #print(mask)
    cv2.imshow("res", res)
    cv2.imshow("final",final)
    cv2.waitKey(0)
