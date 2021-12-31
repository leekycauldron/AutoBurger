import pyautogui
import cv2
import numpy as np
import os, time
from PIL import Image, ImageGrab


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
    images = [["burger1a","burger1b","burger1c"],["burger2a","burger2b","burger2c"],["burger3a","burger3b","burger3c"],["colaa","colab","colac"],["friesa","friesb","friesc"]]
    image_names = ["burger1","burger2","burger3","cola","fries"]
    image_coords = {
        "burger1": burger1,
        "burger2": burger2,
        "burger3": burger3,
        "cola": cola,
        "fries": fries
    }
    #CHANGED: PICTURES WILL BE PROVIDED SINCE THEY ARE DIFFICULT TO SET UP.
    """#Take screenshots of food items and done button. This only needs to run on the first time or if the images are removed (either by user or program).
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
        colaregion = (cola[0]-16,cola[1]-32,cola[0]+16,cola[1]+32)
        img = ImageGrab.grab(colaregion)
        img.save(os.path.join("images", "cola.jpg"))
        img.close()"""


    while True:
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
        lower_black = np.array([0,0,13])
        upper_black = np.array([0,0,240])
        mask = cv2.inRange(imgHSV,lower_black,upper_black)

        for i in range(len(mask)): # iterate each row
            for px in range(len(mask[i])):
        
                if mask[i, px] == 255:
                    #print(final[i][px])
            
                    final[i,px] = (255,255,255) # Change pixel to white if it needs to be removed (part of mask)
        gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 1)
        imgCanny = cv2.Canny(blur, 400, 400//3)
        
        orders = []
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print("CONTOURS FOUND: ", str(len(contours)))
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            print(area)
            if area > 11.5: # Contours are detected in parts of food (discard it).
                cv2.drawContours(final, cnt, -1, (0, 0, 0), 3)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(final, (x,y), (x+w, y+h), (0,255,0), 2)
                # Save each contour to a file
                for i in range(3):
                    temp = img[y:y+h, x:x+w]
                    cv2.imwrite(os.path.join("tmp","tmp.jpg"),temp)
                    diffs_unsorted, diffs = [], []
                    for i in range(5): # loop through each food item.
                        
                        tmp_sum = 0
                        for j in range(3):
                            tmp_image = cv2.imread(os.path.join("images",images[i][j]+".jpg")) # Get the reference image
                            
                            tmp_img = cv2.imread(os.path.join("tmp","tmp.jpg")) # Get the image being compared.
                            y,x,c = tmp_img.shape
                            y1,x1,c1 = tmp_image.shape
                            if y * x > y1 * x1:
                                tmp_image = cv2.resize(tmp_image,(x,y)) # Change the reference image to fit the size of the image being compared to it.
                            elif y * x < y1 * x1:
                                tmp_img = cv2.resize(tmp_img,(x1,y1))
                            
                            
                            tmp_sum += cv2.absdiff(tmp_image,tmp_img).sum()
                        diffs.append(tmp_sum // 3)
                        diffs_unsorted.append(tmp_sum // 3)
                print("DIFFERENCES: " + str(diffs))
                print("DIFFERENCES: ", str(images))
                os.remove(os.path.join("tmp","tmp.jpg"))

                #After the images are compared, get the most matching one and save it to a queue (just a list).
                
                
                diffs.sort()
                print("DIFFERENCES SORTED: " + str(diffs))
                print("DIFFERENCES UNSORTED: " + str(diffs_unsorted))
                print(diffs_unsorted.index(diffs[0]))
         
                orders.append(image_names[diffs_unsorted.index(diffs[0])]) # save the order by getting the index of the image with the least difference.
                
        
        print("Give the customer: " + str(orders))

        #for each order, click it
        for i in range(len(orders)):
            print(image_coords[orders[i]][0])
            pyautogui.click(x=image_coords[orders[i]][0],y=image_coords[orders[i]][1]) # click on item on menu
            time.sleep(1)

        # click done button then wait for next customer
        time.sleep(1)
        pyautogui.click(x=done1[0],y=done1[1])

        time.sleep(5)
  
    
