print("Initializing...")
from userInput import execMenu, init, getTopOrderCoords, getBotOrderCoords, getMenuCoords, getRepeats
from classifier import getOrderImg, getOrderItems, removeText, classifyShape
import os, time, cv2


if __name__ == "__main__":
    #init()
    topCoords= getTopOrderCoords()
    botCoords = getBotOrderCoords()
    menu_coords = getMenuCoords()
    repeats = getRepeats()
    order_region = (topCoords[0],topCoords[1],botCoords[0],botCoords[1])
    while 1: # Main Automation loop
        orders = []
        cnt = 0 
        item_coords = 0
        item_corners = [[] for _ in range(repeats)]
        img = []
        for i in range(repeats):
            img = getOrderImg(order_region) # Get the order
            img = removeText(img) # Remove any text
            cnt, item_coords, corners = getOrderItems(img) # Get order items
            if cnt == 0: continue
            counter = 0
            while True:
                if len(item_corners[counter]) != 0:
                    counter += 1
                else:
                    break
            item_corners[counter] = corners
        corners = []
        
        for i in range(len(item_corners[counter])):
            tmp_sum = 0
            for j in range(repeats):
                try:
                    tmp_sum += item_corners[j][i]
                    print("{} found adding to avg sum for item {}.".format(item_corners[j][i],i))
                except:
                    pass
            corners.append(tmp_sum // repeats) # get the average

        print("There is {} item(s)".format(cnt))
        print(item_coords)
        flag = False
        while True: # In case multiple false positives present, use a loop.
            for i in range(len(item_coords)):
                res = classifyShape(corners[i],"main",item_coords[i])
                item_coords.pop(i)
                if res == "fpos":
                    
                    print("False positive detected.")
                    break
                else:
                    orders.append(res)
                    flag = True
                    break
            if flag: break
        if len(item_coords) > 0:
            for coords in item_coords:
                orders.append(classifyShape(corners[0],"side",coords))
        """
        if cnt == 3: # orders of three always have the following items.
            orders.append("cola")
            orders.append("fries")
            # remove the items from the coords list since we don't need to scan them.
            
            print("Cola and fries automatically added.")
            print("Burger has {} corners".format(corners[0]))

            counter = 0 
            while True: # In case multiple false positives present, use a loop.
                res = classifyShape(corners[counter],"main",item_coords[counter])
                item_coords.pop(counter)
                if res == "fpos":
                    print("False positive detected.")
                    counter += 1
                else:
                    orders.append(res)
                    orders.remove("cola")
                    orders.remove("fries")
                    orders.append(classifyShape(corners[1],"side",item_coords[counter]))
                    item_coords.pop(counter)
                    break
            if len(item_coords) > 0:
                orders.append(classifyShape(corners[0],"side",item_coords[0]))
        
        elif cnt == 2:
            print("Burger has {} corners".format(corners[0]))
            orders.append(classifyShape(corners[0],"main",item_coords[0]))
 
            print("Side has {} corners".format(corners[1]))
            orders.append(classifyShape(corners[1],"side",item_coords[1]))

        elif cnt == 1:
            print("Burger has {} corners".format(corners[0]))
            orders.append(classifyShape(corners[0],"main",item_coords[0]))
        elif cnt == 0:
            print("No customer")
            pass # Something went wrong, trying again...
        else:
            """

        os.remove(os.path.join('tmp','orders.jpg'))
        print(orders)
        time.sleep(0.5)
        try:
            temp = orders.index("fpos")
            print("fpos in orders")
            while orders.index("fpos") != -1:
                orders.remove("fpos")
            execMenu(orders,menu_coords)
        except:
            execMenu(orders,menu_coords)

        time.sleep(5)
