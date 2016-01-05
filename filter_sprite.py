import cv2
import numpy as np
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)

im = cv2.imread(filename, -1)

print(filename)
input("PRESS ENTER TO CONTINUE")

print(im.shape)

#xconst = 49
#yconst = 109
xconst = 1
yconst = 1

w = im.shape[0]/xconst
h = im.shape[1]/yconst

ndir = input("Digite o nome do diretorio para salvar os sprites:")

i = 0
j = 0

while i < h & j < w:
	
	



##################################################################################
def findSprite(beginx, beginy, image):
	x = beginx #the size of a collum
	y = beginy #the begining of the sprite
	j = beginy #the end of the sprite

	i = beginx
	

	while image[x][y] != [255,255,255, 255]:
		x++

	#iterate through the colum looking if every pixel is equal to a transparant line, if not ends the looking
	while image[i][y][4] == 0:
		if i < x:
			i++
		else:
			i = beginx
			y++

	j = y
	flag = 0
	i = beginx

	#iterate through the array looking for a new transparent line
	while flag == 0:

		if i < x & image[i][j][4] == 0:
			i++
		elif i < x & image[i][j][4] != 0:
			#?# add a routine to minimize the image size
			i = beginx
			j++
		else:
			flag = 1
			i = beginx
			j++	

	#the sprite matrix
	buff = image[beginx:x, y:j]

	return buff

##old algorithm###################################################################
def base():
	for i in range(0, h):
		for j in range(0, w):
			#buff = im[j*yconst:(j+1)*yconst, i*xconst:(i+1)*xconst]

			if not os.path.exists(ndir):
				os.makedirs(ndir)
			cv2.imwrite("./"+ndir+"/sprite_"+str(j)+"_"+str(i)+".png", buff)

##################################################################################