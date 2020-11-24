import pyautogui
from datetime import datetime
from mss import mss
import mss.tools as tools
from PIL import Image
import pygetwindow as gw
import numpy
import time as tm
import math
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageOps
from MachineDesktopInterface import MachineDesktopInterface
screenWidth, screenHeight = pyautogui.size() # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)

currentMouseX, currentMouseY = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.

keyState = { key: False for key in pyautogui.KEYBOARD_KEYS }
# pyautogui.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
# pyautogui.click() # Click the mouse at its current location.
# pyautogui.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
# pyautogui.move(100, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
# pyautogui.doubleClick() # Double click the mouse at the
# pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # Use tweening/easing function to move mouse over 2 seconds.
# pyautogui.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
# pyautogui.press('esc') # Simulate pressing the Escape key.
# pyautogui.keyDown('shift')
# pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.hotkey('ctrl', 'c')
mdi = MachineDesktopInterface('Poly Bridge 2', [ 'w', 'a', 's', 'd', 'Should_Move_Mouse', 'Move_To_Mouse_X', pyautogui.PRIMARY])
screenOutput = mdi.getScreenOutputModel()

i = 0
while i < 1:
    time = datetime.now()
    formatted_time = time.strftime('%S%f')
    formatted_time = int(formatted_time[0:2])
    x = 600 + 200 * math.cos(60 * int(formatted_time) * math.pi / 180)
    # y = 10 #600 + 200 * math.sin(60 * int(formatted_time) * math.pi / 180)
    active = [False, False, False, False, False, x, True]
    o = next(screenOutput)
    print(o)
    # plt.imshow(o, cmap='gray')
    # plt.show()
    #mdi.interpretAction(active)
    tm.sleep(1)
    i += 1
# with mss() as sct:
#     # capture the first image
#     screenWidth, screenHeight = pyautogui.size()
    
#     print(window.top, window.left, window.width, window.height)
#     print(screenWidth, screenHeight)
#     print('---------------------')
#     tm.sleep(0.2)

#     monitor = {"top": window.top, "left": window.left + 10, "width": window.width - 20, "height": window.height - 10}
#     sct_img = numpy.array(sct.grab(monitor))
#     sct_img = sct.grab(monitor)
#     tools.to_png(sct_img.rgb, sct_img.size, output='a.png')
#     for i in range(1):
#         now = datetime.now()
#         print(now - time)
#         time = now
#         temp = numpy.array(sct.grab(monitor))
#         # perform actions only on change
#         if not numpy.array_equal(sct_img, temp):
#             sct_img = temp
#             sct_img = sct.grab(monitor)
#             tools.to_png(sct_img.rgb, sct_img.size, output='a' + str(i) + '.png')

        #img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
