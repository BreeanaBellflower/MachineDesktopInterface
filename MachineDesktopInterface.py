from MouseInterface import MouseInterface
from KeyboardInterface import KeyboardInterface
import pygetwindow as gw
import pyautogui
import numpy
from mss import mss

with mss() as sct:
    class MachineDesktopInterface:
        def __init__(self, windowTitle, windowWidth=800, windowHeight=600, observedKeys=None, monitor_number = 1, windowLeftOffset = 10, windowTopOffset = 0, windowWidthOffset = -20, windowHeightOffset = -10):
            if(observedKeys == None):
                observedKeys = []
            self.windowTitle = windowTitle
            self.monitor_number = 1
            self.KEYBOARD_KEYS = pyautogui.KEYBOARD_KEYS
            self.MOUSE_BUTTONS = [ pyautogui.PRIMARY, pyautogui.MIDDLE, pyautogui.SECONDARY ]
            self.MOUSE_POSITION = [ 'Should_Move_Mouse', 'Move_To_Mouse_X', 'Move_To_Mouse_Y', 'Mouse_Offset_X', 'Mouse_Offset_Y' ]
            self.keyboard = KeyboardInterface()
            self.mouse = MouseInterface()
            self.observedKeys = observedKeys
            self.windowWidth = windowWidth
            self.windowHeight = windowHeight
            self.x = 0
            self.y = 0
            pyautogui.FAILSAFE = False
            pyautogui.PAUSE = 0
            for i in observedKeys:
                if i not in self.KEYBOARD_KEYS and i not in self.MOUSE_BUTTONS and i not in self.MOUSE_POSITION:
                    raise Exception("Invalid key or button was supplied to observedKeys")
        
        def getMouse(self):
            return self.mouse
        
        def getKeyboard(self):
            return self.keyboard

        def changeObservedKeys(self, observedKeys=None):
            if(observedKeys == None):
                observedKeys = []
            self.observedKeys = observedKeys

        def changeState(self, keyValues, x, y):
            if(len(keyValues) != len(self.observedKeys)):
                raise Exception("The length of passed in keys does not match the length of observed keys.")
            for (value, key) in (keyValues, self.observedKeys):
                if key in self.KEYBOARD_KEYS:
                    if value:
                        self.keyboard.holdKey(key)
                    else:
                        self.keyboard.releaseKey(key)
                elif key in self.MOUSE_BUTTONS:
                    if value:
                        self.mouse.holdClick(x, y, key)
                    else:
                        self.mouse.releaseClick(x, y, key)

        def setWindowTitle(self, newTitle):
            self.windowTitle = newTitle
            
        def activateWindow(self):
            window = gw.getWindowsWithTitle(self.windowTitle)[0]
            window.activate()
        
        def changeMonitor(self, monitor_number):
            self.monitor_number = monitor_number
        
        def changeWindowSize(self, newWidth, newHeight):
            window = gw.getWindowsWithTitle(self.windowTitle)[0]
            window.activate()
            window.resizeTo(self.windowWidth, self.windowHeight)
            window.moveTo(1,1)

        def updateScreenCaptureZone(self):
            window = gw.getWindowsWithTitle(self.windowTitle)[0]
            mon = sct.monitors(self.monitor_number)
            self.monitor = {mon["top"]: window.top, mon["left"]: window.left + 10, "width": window.width - 20, "height": window.height - 10, "mon": self.monitor_number}

        def getScreenOutput(self):
            with mss() as sct:
                window = gw.getWindowsWithTitle(self.windowTitle)[0]
                window.activate()
                window.resizeTo(self.windowWidth, self.windowHeight)
                window.moveTo(0,0)
                self.x = 0
                self.y = 0
                screenWidth, screenHeight = pyautogui.size()
                pyautogui.moveTo(int(screenWidth),int(screenHeight))
                mon = sct.monitors(self.monitor_number)
                self.monitor = {mon["top"]: window.top, mon["left"]: window.left + 10, "width": window.width - 20, "height": window.height - 10, "mon": self.monitor_number}

                while True:
                    yield numpy.array(sct.grab(self.monitor))
        
        #provide an array of booleans and numbers matching the length and order of observed keys
        def interpretAction(self, activeKeys):
            if len(activeKeys) != len(self.observedKeys):
                raise Exception("Active key array mismatch: provide an array of booleans and numbers matching the length and order of observed keys")
            for i in range(len(activeKeys)):
                if self.observedKeys[i] in self.KEYBOARD_KEYS:
                    if activeKeys[i]:
                        if self.keyboard.getState()[self.observedKeys[i]] != True:
                            self.keyboard.holdKey(self.observedKeys[i])
                    else:
                        if self.keyboard.getState()[self.observedKeys[i]] == True:
                            self.keyboard.releaseKey(self.observedKeys[i])
                else:
                    try:
                        index = self.observedKeys.index('Should_Move_Mouse')
                        if activeKeys[index] == True:
                            if self.observedKeys[i] == 'Move_To_Mouse_X':
                                self.x = activeKeys[i]
                            elif self.observedKeys[i] == 'Mouse_Offset_X':
                                self.x = self.x + activeKeys[i]
                            elif self.observedKeys[i] == 'Move_To_Mouse_Y':
                                self.y = activeKeys[i]
                            elif self.observedKeys[i] == 'Mouse_Offset_Y':
                                self.y = self.y + activeKeys[i]
                            self.mouse.moveTo(self.x, self.y)
                    except ValueError:
                        pass

                    if self.observedKeys[i] in self.MOUSE_BUTTONS:
                        if activeKeys[i]:
                            self.mouse.holdClick(self.x, self.y, button=self.observedKeys[i])
                        else:
                            self.mouse.releaseClick(self.x, self.y, self.observedKeys[i])