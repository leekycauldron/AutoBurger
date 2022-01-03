import pyautogui
import time
from pynput.mouse import Button, Controller


mouse = Controller()

menu_coords = {}
def init():
    print("AutoBurger v2 running...\n\n")
    input("Change your camera angle to match the one in the reference image. \nHIT *ENTER* WHEN DONE...")


# Get the coordinates for where on the screen the customer orders are.
def getTopOrderCoords(): 
    input("Place your cursors at the top left of where the customer orders start. (Ignore greeting)\nHIT *ENTER* WHEN DONE...")
    return pyautogui.position()

def getBotOrderCoords(): 
    input("Place your cursors at the bottom right of where the customer orders end.\nHIT *ENTER* WHEN DONE...")
    return pyautogui.position()

def getMenuCoords():
    input("Place your cursors on the single cheeseburger on the menu\nHIT *ENTER* WHEN DONE...")
    menu_coords["burger1"] = pyautogui.position()
    input("Place your cursors on the double cheeseburger on the menu\nHIT *ENTER* WHEN DONE...")
    menu_coords["burger2"] = pyautogui.position()
    input("Place your cursors on the deluxe cheeseburger on the menu\nHIT *ENTER* WHEN DONE...")
    menu_coords["burger3"] = pyautogui.position()
    input("Place your cursors on the fries on the menu\nHIT *ENTER* WHEN DONE...")
    menu_coords["fries"] = pyautogui.position()
    input("Place your cursors on the cola on the menu\nHIT *ENTER* WHEN DONE...")
    menu_coords["cola"] = pyautogui.position()
    input("Place your cursors on the done button on the menu\nHIT *ENTER* WHEN DONE...")
    menu_coords["done"] = pyautogui.position()

    return menu_coords

def execMenu(orders, menu_coords): # Execute items

    #for each order, click it
    for i in range(len(orders)):
        
        mouse.position = menu_coords[orders[i]]
        time.sleep(0.1)
        mouse.click(Button.left, 2)
        time.sleep(0.1)
        with pyautogui.hold("alt"):
            time.sleep(0.1)
            pyautogui.press("tab")
        time.sleep(0.1)


    mouse.position = menu_coords["done"]
    time.sleep(0.1)
    with pyautogui.hold("alt"):
            time.sleep(0.1)
            pyautogui.press("tab")
    time.sleep(0.1)
    mouse.click(Button.left, 2)
    time.sleep(0.1)
    with pyautogui.hold("alt"):
            time.sleep(0.1)
            pyautogui.press("tab")
    time.sleep(0.1)
