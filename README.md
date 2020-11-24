**The Machine Desktop Interface**

A tool to turn ML outputs into meaningful actions within windowed desktop applications on Windows or Mac machines.

The setup is shown below:

1. Open the application you want to interact with and, if possible, place it in windowed mode. The smaller form will speed up MSS code (which supplies screen data as input, for example, to a neural network).

EXAMPLE:

mdi = MachineDesktopInterface('my application name', ['w', 'a', 's', 'd'])

> while True:  
> &nbsp;&nbsp;&nbsp;&nbsp; screenOutput = getScreenOutputModel(800, 600)  
> &nbsp;&nbsp;&nbsp;&nbsp; screenCapture = next(screenOutput)  
> &nbsp;&nbsp;&nbsp;&nbsp; \#input screen capture's numpy data as input to a neural network, get 4 outputs  
> &nbsp;&nbsp;&nbsp;&nbsp; \#output = [0.2, 0.3, 0.9, 0.3]  
> &nbsp;&nbsp;&nbsp;&nbsp; \#transform your list into a list of booleans and floats according to the type of input  
> &nbsp;&nbsp;&nbsp;&nbsp; \#interfaceInput = [False, False, True, False]  
> &nbsp;&nbsp;&nbsp;&nbsp; mdi.interpretAction(interfaceInput)  
