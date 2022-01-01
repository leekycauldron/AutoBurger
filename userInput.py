import pyautogui


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
    