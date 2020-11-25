import pyautogui

class MouseInterface:
    def __init__(self):
        self.mouseState = {
            pyautogui.PRIMARY: False,
            pyautogui.MIDDLE: False,
            pyautogui.SECONDARY: False
        }

    def singleClick(self, x, y, button=pyautogui.PRIMARY, duration=0.0):
        pyautogui.click(x, y, button=button, duration=duration)
        return self.mouseState

    def doubleClick(self, x, y, button=pyautogui.PRIMARY, duration=0.0):
        pyautogui.doubleClick(x, y, button=button, duration=duration)
        return self.mouseState

    def tripleClick(self, x, y, button=pyautogui.PRIMARY, duration=0.0):
        pyautogui.tripleClick(x, y, button=button, duration=duration)
        return self.mouseState
    
    def holdClick(self, x, y, button=pyautogui.PRIMARY, duration=0.0):
        pyautogui.mouseDown(x, y, button=button, duration=duration)
        self.mouseState[button] = True
        return self.mouseState
    
    def releaseClick(self, x, y, button=pyautogui.PRIMARY, duration=0.0):
        pyautogui.mouseUp(x, y, button=button, duration=duration)
        self.mouseState[button] = False
        return self.mouseState

    def moveTo(self, x, y):
        pyautogui.moveTo(x, y)
        return self.mouseState

def _test():
    assert 1 + 1 == 2

if __name__ == '__main__':
    _test()