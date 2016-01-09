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


#find the character sprite position
def find_char_pos(initx, inity, image, zero):
	#variable declaration --python is not magic, please...
	posx = initx
	posy = inity

	contx = initx
	#conty = inity
	conty = zero
	i = initx
	j = inity

	k = 0
	l = 0

	h = image.shape[0]
	w = image.shape[1]

	#find the bottom white line
	while (image[contx][zero][3] == 0):
		if (contx >= h):
			return [ -1, contx, -1, -1]
		contx += 1


	#find the right white colum
	#while (image[initx][conty][3] == 0):
	while (image[initx][conty][3] == 0):
		if (conty >= w):
			return [ -1, contx, -1, -1]
		conty += 1

	#normalize
	conty -= 1
	contx -= 1

	#check all the lines in the interval initx contx
	# |
	# |
	# |
	# v
	#find the begining of the upper part of the sprite
	for k in range(0,3):
		if (k%2 == 0):
			while ((isHomogenious(0, i, inity, conty, image)) == 0):
				if (i >= contx):
					return [ -1, contx, -1, -1]
					#return [ -1, contx, -1, conty]
				i += 1
		elif (k%2 == 1):
			while ((isHomogenious(0, i, inity, conty, image)) == 1):
				if (i >= contx):
					return [ -1, contx, -1, -1]
					#return [ -1, contx, -1, conty]
				i += 1

	#check the colums up to find the next sprite
	for l in range(0,2):
		while ((isHomogenious(1, j, i, contx, image)) == 1):
			if (j >= conty)&(j < image.shape[1]):
				return [ -1, contx, -1, conty+3]
			elif (j >= conty)&(j >= image.shape[1]):
				return [ -1, contx, -1, -1]
			j += 1

	l = j
	#check the colums up to find the end of the sprite
	while ((isHomogenious(1, l, i, contx, image)) == 0):
		if (l >= conty)&(l < image.shape[1]):
			return [ -1, contx, -1, conty+2]
		elif (l >= conty)&(l >= image.shape[1]):
			return [ -1, contx, -1, -1]
		l += 1	

	#i -> the beginning of the sprite line
	#j -> the beginning of the sprite colum
	#l -> the end of the sprite colum

	#pos = np.array([i, contx, j, l])
	pos = [i, contx, j, l]

	return pos


##GUI do Script###################################################################
# we don't want a full GUI, so keep the root window from appearing
Tk().withdraw() 

# show an "Open" dialog box and return the path to the selected file
##define the file control parts
filename = askopenfilename() 
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

h = 0
w = 0

wc = 0
hc = 0

sflag = 0
zero = 0

#loop as long the image existis
while h < newim.shape[0]:
	while w < newim.shape[1]:
		frame_pos = find_char_pos(h,w,newim, zero)
		if (frame_pos[2] == -1):
			if (frame_pos[3] == -1):
				break
			else:
				sflag = 1
				w = frame_pos[3]
				zero = frame_pos[3]
				break

		frame = newim[frame_pos[0]:frame_pos[1], frame_pos[2]:frame_pos[3]]
		#cv2.imwrite(ndir+"/"+"test"+".png", frame)
		#filename = ndir+"/img_"+str(h)+"_"+str(w)+".png"
		filename = ndir+"/img_"+str(hc)+"_"+str(wc)+".png"
		cv2.imwrite(filename, frame)
		print(str(frame_pos) + " - " + str(hc)+"_"+str(wc))

		if(os.stat(filename).st_size <= 1):
			os.system("rm "+filename)
		else:
			wc += 1
		
		w = frame_pos[3]+1
		

	
	h = frame_pos[1] + 2
	if(sflag == 0):
		w = 0
	elif(sflag == 1):
		sflag = 0
	hc += 1
	wc = 0
