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
	#rotina para realizar o procedimento por toda a imagem
	



##################################################################################
def findSprite(beginx, beginy, image):
    x = beginx #the size of a collum
    y = beginy #the begining of the sprite
    j = beginy #the end of the sprite

    i = beginx
    
    #find the white line under all sprites
    while image[x][y] != [255,255,255, 255]:
        x++

    #iterate through the colum looking if every pixel is equal to a transparant line, if not ends the looking
    #because we found the first line in the sprite


    #while the colums are homogenius, because when they find a non homogenius line it is the begining of the sprite
    while isHomogenious(1, y, beginx, x, image):
        y++

    j = y
    flag = 0
    i = beginx

    #iterate through the array looking for a new transparent line
    while not isHomogenious(1, j, beginx, x, image):
        j++

    #the sprite matrix
    buff = image[beginx:x, y:j]

    return buff


#check if a delimited line or colum defined by [posb, pose] is homogenious and return it
#loc = 0: line
#loc = 1: colum
def isHomogenious(loc, pos, posb, pose, image):

    flag = 1
    for i in range(posb, pose):
        if loc == 0:
            if image[pos][i] != image[pos][i+1]:
                flag = 0
                break
        else:
            if image[i][pos] != image[i+1][pos]:
                flag = 0
                break

    return flag

##old algorithm###################################################################
def base():
	for i in range(0, h):
		for j in range(0, w):
			#buff = im[j*yconst:(j+1)*yconst, i*xconst:(i+1)*xconst]

			if not os.path.exists(ndir):
				os.makedirs(ndir)
			cv2.imwrite("./"+ndir+"/sprite_"+str(j)+"_"+str(i)+".png", buff)

##################################################################################
