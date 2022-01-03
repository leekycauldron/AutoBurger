print("Initializing...")
from userInput import execMenu, init, getTopOrderCoords, getBotOrderCoords, getMenuCoords
from classifier import getOrderImg, getOrderItems, removeText, classifyShape
import os, time, cv2


if __name__ == "__main__":
    init()
    topCoords= getTopOrderCoords()
    botCoords = getBotOrderCoords()
    menu_coords = getMenuCoords()
  
    order_region = (topCoords[0],topCoords[1],botCoords[0],botCoords[1])

    while 1: # Main Automation loop
        orders = []
    
        item_coords = 0
        
        img = []
        img = getOrderImg(order_region) # Get the order
        img = removeText(img) # Remove any text
        cnt, item_coords = getOrderItems(img) # Get order items
        
        flag = False
        while True: # In case multiple false positives present, use a loop.
            if len(item_coords) > 0:
                for i in range(len(item_coords)):
                    res = classifyShape("main",item_coords[i])
                    item_coords.pop(i)
                    if res == "fpos": break
                    else:
                        orders.append(res)
                        flag = True
                        break
            else: break  
            if flag: break
        if len(item_coords) > 0:
            for coords in item_coords:
                orders.append(classifyShape("side",coords))

        os.remove(os.path.join('tmp','orders.jpg'))
        print(orders)
        time.sleep(0.5)
        try:
            temp = orders.index("fpos")
            while orders.index("fpos") != -1:
                orders.remove("fpos")
            execMenu(orders,menu_coords)
        except:
            execMenu(orders,menu_coords)

        time.sleep(5)
