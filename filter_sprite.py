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

nextx = 0
nexty = 0
buffx = 0


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


##################################################################################
def findSprite(beginx, beginy, image):
	#cv2.imshow("inf",image)

	#the size of a collum
	x = beginx 
	#the begining of the sprite
	y = beginy 
	#the end of the sprite
	j = beginy 
	i = beginx

	global nextx
	global nexty
	global buffx
    
	sumbuff = 0

	if (buffx == nextx):
		sumbuff = 1

	#find the white line under all sprites
	print(image[x][y])

	while ((image[x][y] == [136,136,112,255]).all())|((image[x][y] == [136,136,112,0]).all())&(x < image.shape[0]):
		x += 1
		if sumbuff == 1:
			buffx += 1
		#print(x)

	#normalize the values(cutoff the white line for sure)
	x -= 2

	#iterate through the colum looking if every pixel is equal to a transparant line, if not ends the looking
	#because we found the first line in the sprite

	#while the colums are homogenius, because when they find a non homogenius line it is the begining of the sprite
	#hom = isHomogenious(1, y, beginx, x, image)
	#print("y:"+str(y)+" bx:"+str(beginx)+" x:"+str(x))
	nextflag = 0
	while (nextflag < 3 )&(y < image.shape[1]):

		if(isHomogenious(1, y, beginx, x, image) == 0 ):
			nextflag += 1
		else:
			nextflag = 0
		y += 1
		#print("y: "+str(y))

	y -= 3 #normalization for y
	j = y
	flag = 0
	i = beginx

	#iterate through the array looking for a new transparent line
	while (isHomogenious(1, j, beginx, x, image) == 0):
		j += 1
		#print("j: "+str(j))


	#pass the values obtained to the global variables
	#nextx = x+2
	#buffx = x+4
	nextx = 0
	nexty = j+4
	#the sprite matrix
	buff = image[beginx:x, y:j]

	return buff


##old algorithm####
###############################################################
def base():
	for i in range(0, h):
		for j in range(0, w):
			#buff = im[j*yconst:(j+1)*yconst, i*xconst:(i+1)*xconst]

			if not os.path.exists(ndir):
			    os.makedirs(ndir)
			cv2.imwrite("./"+ndir+"/sprite_"+str(j)+"_"+str(i)+".png", buff)

##################################################################################




Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing


##define the file control parts
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)
ndir = raw_input("Digite o nome do diretorio para salvar os sprites:")
if not os.path.exists(ndir):
    os.makedirs(ndir)


img = cv2.imread(filename, -1)

b_channel, g_channel, r_channel = cv2.split(img)
alpha_channel = np.ones((img.shape[0], img.shape[1]), img.dtype)*255

newim = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

h = newim.shape[0]
w = newim.shape[1]

#turns the entire image transparent
for i in range(0, newim.shape[0]):
	for j in range(0, newim.shape[1]):
		#print(im[i][j])
		if (newim[i][j] == [136,136,112,255]).all():
			#newim[i][j][3] = 0
			newim[i][j][3] = 0


print(filename)
raw_input("PRESS ENTER TO CONTINUE")

print(newim.shape)
cv2.imwrite(ndir+"/buff.png", newim)



##imp = findSprite(nextx,nexty,newim)
#xconst = 49
#yconst = 109
xconst = 1
yconst = 1

#w = im.shape[0]/xconst
#h = im.shape[1]/yconst

##cv2.imwrite(ndir+"/img_"+str(beginx)+"_"+str(beginy)+".png", imp)

h = nextx
w = nexty

imgcounterx = 0
imgcountery = 0
soma = 0

while h < newim.shape[0]:
	while w < newim.shape[1]:

		imp = findSprite(nextx,nexty,newim)
		filename = ndir+"/img_"+str(imgcounterx)+"_"+str(imgcountery)+".png"
		cv2.imwrite(filename, imp)
		if os.stat(filename).st_size <= 2:
			os.system("rm "+filename)
		else:
			imgcountery += 1

		h = nextx
		w = nexty


	nextx = buffx
	nexty = 0
	w = 0
	imgcounterx += 1
	imgcountery = 0
	print("nx: "+str(nextx)+" / ny: "+str(nexty))

#rotina para realizar o procedimento por toda a imagem