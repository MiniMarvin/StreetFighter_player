import cv2
import numpy as np
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)

im = cv2.imread(filename)

print(filename)
input("PRESS ENTER TO CONTINUE")

print(im.shape)

xconst = 49
yconst = 109

w = im.shape[0]/xconst
h = im.shape[1]/yconst

ndir = input("Digite o nome do diretorio para salvar os sprites:")

for i in range(0, h):
	for j in range(0, w):
		buff = im[j*yconst:(j+1)*yconst, i*xconst:(i+1)*xconst]
		if not os.path.exists(ndir):
			os.makedirs(ndir)
		cv2.imwrite("./"+ndir+"/sprite_"+str(j)+"_"+str(i)+".png", buff)