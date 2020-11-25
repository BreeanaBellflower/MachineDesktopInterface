from Interfaces.KeyboardInterface import KeyboardInterface
from Interfaces.MouseInterface import MouseInterface
import pygetwindow as gw
import pyautogui
import numpy
from mss import mss

with mss() as sct:
    class MachineDesktopInterface:
        def __init__(self, windowTitle, observedKeys=None, monitor_number = 1, windowLeftOffset = 10, windowTopOffset = 0, windowWidthOffset = -20, windowHeightOffset = -10):
            if(observedKeys == None):
                observedKeys = []
            self.windowTitle = windowTitle
            self.monitor_number = monitor_number
            self.KEYBOARD_KEYS = pyautogui.KEYBOARD_KEYS
            self.MOUSE_BUTTONS = [ pyautogui.PRIMARY, pyautogui.MIDDLE, pyautogui.SECONDARY ]
            self.MOUSE_POSITION = [ 'Should_Move_Mouse', 'Move_To_Mouse_X', 'Move_To_Mouse_Y', 'Mouse_Offset_X', 'Mouse_Offset_Y' ]
            self.keyboard = KeyboardInterface()
            self.mouse = MouseInterface()
            self.observedKeys = observedKeys
            self.x = 0
            self.y = 0
            pyautogui.FAILSAFE = False
            pyautogui.PAUSE = 0

            for i in observedKeys:
                if i not in self.KEYBOARD_KEYS and i not in self.MOUSE_BUTTONS and i not in self.MOUSE_POSITION:
                    raise Exception("Invalid key or button was supplied to observedKeys")
        
        ### Get Direct Access to the Mouse Interface
        def getMouse(self):
            """Get Direct Access to the Mouse Interface"""
            return self.mouse
        
        ### Get Direct Access to the Keyboard Interface
        def getKeyboard(self):
            """Get Direct Access to the Keyboard Interface"""
            return self.keyboard

        ### Change which keys are being observed or the order they are being observed in
        def changeObservedKeys(self, observedKeys=None):
            """Change which keys are being observed or the order they are being observed in"""
            if(observedKeys == None):
                observedKeys = []
            self.observedKeys = observedKeys

        ### Change the window which is being observed
        def setWindowTitle(self, newTitle):
            """Change the window which is being observed"""
            self.windowTitle = newTitle
            self.activateWindow()
        
        ### Open and focus on a window
        def activateWindow(self):
            """Open and focus on a window"""
            window = None
            try:
                window = gw.getWindowsWithTitle(self.windowTitle)[0]
            except IndexError:
                raise Exception("The window with title " + self.windowTitle + " does not exist")
            window.restore()
            window.show()
            window.activate()
            window.resizeTo(self.width, self.height)
            window.moveTo(0,0)
            self.width = window.width
            self.height = window.height
        
        ### Change the monitor that is being used
        def changeMonitor(self, monitor_number):
            """Change the monitor that is being used"""
            self.monitor_number = monitor_number
        
        ### Change the application window size
        def changeWindowSize(self, newWidth, newHeight):
            """Change the application window size"""
            self.width = newWidth
            self.height = newHeight
            self.activateWindow()

        ### Update the capture zone -- changes the monitored area to allow for cropping
        def updateScreenCaptureZone(self):
            """Update the capture zone -- changes the monitored area to allow for cropping"""
            window = None
            try:
                window = gw.getWindowsWithTitle(self.windowTitle)[0]
            except IndexError:
                raise Exception("The window with title " + self.windowTitle + " does not exist")
            mon = sct.monitors(self.monitor_number)
            self.monitor = {'top': mon["top"] + window.top, 'left': mon["left"] + window.left + 10, "width": window.width - 20, "height": window.height - 10, "mon": self.monitor_number}

        ### Get a generator that returns a numpy array of screen captures of the application
        def getScreenOutputModel(self, width = None, height = None):
            """Get a generator that returns a numpy array of screen captures of the application.\n
            \nCalling next on the generator while the application window is not visible will render the generator inert -- stopIteration will be thrown."""
            with mss() as sct:
                window = None
                try:
                    window = gw.getWindowsWithTitle(self.windowTitle)[0]
                except IndexError:
                    raise Exception("The window with title " + self.windowTitle + " does not exist")
                window.restore()
                window.show()
                window.activate()
                if(width != None and height != None):
                    window.resizeTo(width, height)
                    self.width = width
                    self.height = height
                else:
                    self.width = window.width
                    self.height = window.height
                window.moveTo(0,0)
                self.x = 0
                self.y = 0
                screenWidth, screenHeight = pyautogui.size()
                pyautogui.moveTo(int(screenWidth),int(screenHeight))
                mon = sct.monitors[self.monitor_number]
                self.monitor = {'top': mon["top"] + window.top, 'left': mon["left"] + window.left + 10, "width": window.width - 20, "height": window.height - 10, "mon": self.monitor_number}

                while True:
                    if window.visible:
                        yield numpy.array(sct.grab(self.monitor))
                    else:
                        return
        
        ### Provide an array of booleans and numbers matching the length and order of observed keys, and perform actions according to the action values supplied
        def interpretAction(self, actionValues):
            """Provide an array of action values matching the length and order of observed keys, and perform actions according to the action values supplied.\n
            \nIf the observedKeys list is ['w', 'a', 's', 'd'], then supplying a list of action values [False, False, True, False] to this method will press the 's' key."""
            if len(actionValues) != len(self.observedKeys):
                raise Exception("Active key array mismatch: provide an array of booleans and numbers matching the length and order of observed keys")
            for i in range(len(actionValues)):
                if self.observedKeys[i] in self.KEYBOARD_KEYS:
                    if actionValues[i]:
                        if self.keyboard.getState()[self.observedKeys[i]] != True:
                            self.keyboard.holdKey(self.observedKeys[i])
                    else:
                        if self.keyboard.getState()[self.observedKeys[i]] == True:
                            self.keyboard.releaseKey(self.observedKeys[i])
                else:
                    window = None
                    try:
                        window = gw.getWindowsWithTitle(self.windowTitle)[0]
                    except IndexError:
                        raise Exception("The window with title " + self.windowTitle + " does not exist")
                    try:
                        index = self.observedKeys.index('Should_Move_Mouse')
                        if actionValues[index] == True:
                            if self.observedKeys[i] == 'Move_To_Mouse_X':
                                self.x = actionValues[i]
                            elif self.observedKeys[i] == 'Mouse_Offset_X':
                                self.x = self.x + actionValues[i]
                            elif self.observedKeys[i] == 'Move_To_Mouse_Y':
                                self.y = actionValues[i]
                            elif self.observedKeys[i] == 'Mouse_Offset_Y':
                                self.y = self.y + actionValues[i]
                            
                            if self.x > 1.0:
                                self.x = 1.0
                            if self.x < 0.0:
                                self.x = 0.0

                            if self.y > 1.0:
                                self.y = 1.0
                            if self.y < 0.0:
                                self.y = 0.0

                            self.mouse.moveTo(self.x * self.width + window.left, self.y * self.height + window.top)
                    except ValueError:
                        pass

                    if self.observedKeys[i] in self.MOUSE_BUTTONS:
                        if actionValues[i]:
                            self.mouse.singleClick(self.x + window.left, self.y + window.top, button=self.observedKeys[i])
                        else:
                            self.mouse.releaseClick(self.x + window.left, self.y + window.top, self.observedKeys[i])
