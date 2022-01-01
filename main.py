print("Initializing...")
from userInput import init, getTopOrderCoords, getBotOrderCoords
from classifier import getOrderImg, getOrderItems, removeText, classifyShape
import os


if __name__ == "__main__":
    #init()
    topCoords= getTopOrderCoords()
    botCoords = getBotOrderCoords()
    order_region = (topCoords[0],topCoords[1],botCoords[0],botCoords[1])
    while 1: # Main Automation loop
        orders = []
        img = getOrderImg(order_region) # Get the order
        img = removeText(img) # Remove any text
        cnt, item_coords, corners = getOrderItems(img) # Get order items
        print("There is {} item(s)".format(cnt))
        print(item_coords)

        if cnt == 3: # orders of three always have the following items.
            orders.append("cola")
            orders.append("fries")
            # remove the items from the coords list since we don't need to scan them.
            item_coords.pop(2)
            item_coords.pop(1)
            corners.pop(2)
            corners.pop(1)
            print("Cola and fries automatically added.")
            print("Burger has {} corners".format(corners[0]))
            print(classifyShape(corners[0],"burger"))
        
        elif cnt == 2:
            print("Burger has {} corners".format(corners[0]))
            print(classifyShape(corners[0],"burger"))
            print("Side has {} corners".format(corners[1]))
            print(classifyShape(corners[1],"side"))

        elif cnt == 1:
            print("Burger has {} corners".format(corners[0]))
            print(classifyShape(corners[0],"burger"))
        else:
            print("No customer")
        input("YES: ")
