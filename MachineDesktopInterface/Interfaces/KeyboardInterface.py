import pyautogui

class KeyboardInterface:
    def __init__(self):
        self.keyState = { key: False for key in pyautogui.KEYBOARD_KEYS }

    def pressKey(self, key):
        pyautogui.press(key)
        return self.keyState
    
    def holdKey(self, key):
        pyautogui.keyDown(key)
        self.keyState[key] = True
        return self.keyState
    
    def releaseKey(self, key):
        pyautogui.keyUp(key)
        self.keyState[key] = False
        return self.keyState
    
    def releaseAllKeys(self):
        for key in pyautogui.KEYBOARD_KEYS:
            pyautogui.keyUp(key)
        self.keyState = { key: False for key in pyautogui.KEYBOARD_KEYS }
        return self.keyState
    
    def write(self, message, interval=0.0):
        pyautogui.write(message, interval=interval)
        return self.keyState
    
    def getState(self):
        return self.keyState

def _test():
    assert 1 + 1 == 2

if __name__ == '__main__':
    _test()