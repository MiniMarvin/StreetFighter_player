#############################################
#@Authors: Caio M. Gomes && Michael Barney	#
#Portable version of atack.py				#
#Developed using PyAutoGUI package			#
#############################################

import pyautogui as pa
import time

raw_input("PRESS ENTER TO CONTINUE")

for i in range (10, 0):
    print(str(i)+"\n")
    time.sleep(1)

pa.keyDown("right")

for i in range(0, 100):
	pa.keyDown("a")
	time.sleep(0.25)
	pa.keyUp("a")
	time.sleep(0.25)
	print("punch")

pa.KeyUp("right")

raw_input("exit")