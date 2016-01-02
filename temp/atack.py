import time
import ctypes
import keyboard as keybd

input("press enter to start")

left = 0xCB
up = 0xC8
right = 0xCD
down = 0xD0
a = 0x1E

for i in range (10):
    print(i)
    time.sleep(1)

keybd.PressKey(right)

for i in range (100):
    keybd.PressKey(a)
    time.sleep(0.25)
    keybd.ReleaseKey(a)
    time.sleep(0.25)
    print("punch")

keybd.ReleaseKey(right)

input ("exit")
