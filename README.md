**The Machine Desktop Interface**

A tool to turn ML outputs into meaningful actions within windowed desktop applications on Windows or Mac machines.

The setup is shown below:

1. Open the application you want to interact with and, if possible, place it in windowed mode. The smaller form will speed up MSS code (which supplies screen data as input, for example, to a neural network).

EXAMPLE:

mdi = MachineDesktopInterface('my application name', ['w', 'a', 's', 'd'])

while True:
    screenOutput = getScreenOutputModel(800, 600)
    screenCapture = next(screenOutput)
    \#input screen capture's numpy data as input to a neural network, get 4 outputs
    \#output = [0.2, 0.3, 0.9, 0.3]
    \#transform your list into a list of booleans and floats according to the type of input
    \#interfaceInput = [False, False, True, False]
    mdi.interpretAction(interfaceInput)