import pythoncom,pyHook
import ctypes 
import KeysRecorded
from numpy import savetxt
from time import time

times = []
ascii = []
timeInit = time() 
kr = KeysRecorded.values_recorded
 
def OnKeyboardEvent(event):
    if event.Ascii==92:
        savetxt("TimeData.txt" ,times , delimiter = ",")
        savetxt("KeyData.txt" ,ascii , delimiter = ",")
        ctypes.windll.user32.MessageBoxA(0, "Keyboard recorder stopped", "Keyboard Recorder", 1)
        exit()
    
    for i in range(len(kr)):
        if(kr[i][0]==event.Ascii):
            ascii.append(kr[i][0])
            times.append(time()-timeInit)
    return
            
# create a hook manager object        
ctypes.windll.user32.MessageBoxA(0, "Keyboard recorder started. Press \ to stop", "Keyboard Recorder", 1)
hm=pyHook.HookManager()
hm.KeyDown=OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()