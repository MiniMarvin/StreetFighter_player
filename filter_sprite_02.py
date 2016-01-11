#########################################################
#														#
#@Author: Caio M. Gomes									#
#@Brif: Script to extract some sprites from a sprite	#
#sheet of street fighter II. Necessary to build the		#
#street fighter player AI								#
#														#
#########################################################

import cv2
import numpy as np
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename
import Image


#check if a delimited line or colum defined by [posb, pose] is homogenious and return it
#loc = 0: line
#loc = 1: colum
def isHomogenious(loc, pos, posb, pose, image):

	flag = 1
	#print("inside ih/ b:"+str(posb)+" e:"+str(pose))
	for i in range(posb, pose):
		#print(str(image[i][pos])+","+str(image[i+1][pos]))
		if(flag == 1):
			if loc == 0:
				if (image[pos][i] != image[pos][i+1]).all():
					flag = 0
			else:
				if (image[i][pos] != image[i+1][pos]).all():
					flag = 0

	return flag

def findWhiteLines(initx, image):
	#variable declaration --python is not magic, please...
	contx = initx #position in vertical
	conty = 0 #position in horizontal

	print("---------------------------")

	#define the process limits
	h = image.shape[0]
	w = image.shape[1]

	#find the bottom white line
	while (image[contx][0][3] == 0):
		print("px "+str(contx)+": "+str(image[contx][0][3]))
		if (contx >= h):
			#return -1
			contx = h-1
			break
		contx += 1

	print("line found at: "+str(contx))

	#find the right white colum
	#while (image[initx][conty][3] == 0):
	while (image[initx][conty][3] == 0):
		if (conty >= w):
			return -1
		conty += 1

	print("colum found at: "+str(conty))
	#the position of the white colum and white line
	#divided by regions

	return contx, conty


def findText(initx, endy, image):

	inity = 1
	i = initx
	#check all the lines in the interval initx contx
	# |
	# |
	# |
	# v
	#find the end of the text
	for k in range(0,2):
		if (k%2 == 0):
			while ((isHomogenious(0, i, inity, endy, image)) == 1):
				if (i >= image.shape[0]):
					return -1
				i += 1
		elif (k%2 == 1):
			while ((isHomogenious(0, i, inity, endy, image)) == 0):
				if (i >= image.shape[0]):
					return -1
				i += 1

	print("text found at: "+str(i))
	return i

#follow a horizontal line looking for every sprite in this area
def findSprites(initx, endx, ln, directory, image):
	
	inity = 1

	i = 0 #current position of the colum
	j = 0 #initial position of the current sprite

	brcont = 0 #break counter
	spcont = 0 #sprite status counter
	sncont = 0 #the number of sprites

	while 1:
		##check if we are no longer in a valid area of the image################
	
		if i >= image.shape[1]:
			print("breaked at(1): "+str(i))
			break
		#if (isHomogenious(1, i, initx, endx, image) == 1)&(image[i][initx+10][3] == 255):
		#	brcont += 1
		#else:
		#	brcont = 0

		if brcont == 5:
			print("breaked at(2): "+str(i))
			break
		########################################################################
		
		##find the sprite (h(1)-nh(0)-h(1)) (h->homogeneous)
		if (isHomogenious(1, i, initx, endx, image) == 0)&(spcont <2):
			spcont += 1
			j = i
			inity = 1

		elif (isHomogenious(1, i, initx, endx, image) == 1)&(spcont == 2):
			print(str(initx)+":"+str(endx)+","+str(j)+":"+str(i))
			subim = image[initx:endx, j:i]
			cv2.imwrite(directory+"/img_"+str(ln)+"_"+str(sncont)+".png", subim)
			sncont += 1
			spcont = 0
		elif (spcont < 2):
			spcont = 0

		i += 1
	cv2.imwrite(directory+"/img(t)_"+str(ln)+"_"+str(sncont)+".png", image[initx:endx, j:i])


##GUI do Script###################################################################
# we don't want a full GUI, so keep the root window from appearing
Tk().withdraw() 

# show an "Open" dialog box and return the path to the selected file
##define the file control parts
filename = askopenfilename()

#ext = filename.split(".")[len(filename.split("."))-1]
##convert the image to PNG#########################################################
im = Image.open(filename)
filename = filename.replace(".gif",".png")
im.save(filename,'PNG')
###################################################################################

#print(filename)
ndir = raw_input("Digite o nome do diretorio para salvar os sprites:")
if not os.path.exists(ndir):
    os.makedirs(ndir)

#read the selected file
img = cv2.imread(filename, -1)

#split the image in your color channels
b_channel, g_channel, r_channel = cv2.split(img)
alpha_channel = np.ones((img.shape[0], img.shape[1]), img.dtype)*255
#put an alpha channel into the image
newim = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

#get the image borders
#h = newim.shape[0]
#w = newim.shape[1]

pxo = np.array(newim[2][2])
#turns the entire image transparent
for i in range(0, newim.shape[0]):
	for j in range(0, newim.shape[1]):
		#print(im[i][j])
		if (newim[i][j] == pxo).all():
			newim[i][j][3] = 0


print(filename)
print(newim.shape)

cv2.imwrite(ndir+"/buff.png", newim)
###################################################################################

#define the limits
h = newim.shape[0]
w = newim.shape[1]

linecount = 0 #number of acquired lines

currx = 0 #the current vertical position
curry = 0 #the current white colum position(horizontal)
nextx = 0 #the nex vertical position
beginim = 0 #the position after the text

while currx < h:
	nextx, curry = findWhiteLines(currx, newim)
	if (nextx > 0)&(curry > 0):
		try:
			beginim = findText(currx, curry-2, newim)
			findSprites(beginim, nextx-2, linecount, ndir, newim)

			linecount += 1
			currx = nextx+2
		except:
			print("out of image range!")
			break
	else:
		print("error finding lines!")
		break
		
