import time
import pyscreenshot as ps
import cv2
import numpy as np
from matplotlib import pyplot as plt
import win32gui

MIN_MATCH_COUNT = 4

#Pre Load
#Query Image
img1 = cv2.imread('sprites/idle.png',0)          # queryImage
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
# Find Key Points
kp1, des1 = sift.detectAndCompute(img1,None)

#allow interative mode
plt.ion()

#set boundingbox for game
toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)
window= [(hwnd, title) for hwnd, title in winlist if 'zsnes' in title.lower()]
# just grab the hwnd for first window matching firefox
window = window[0]
hwnd = window[0]
bbox = win32gui.GetWindowRect(hwnd)


input("Press Enter to Start")
#loop
for i in range (5):
    print("Current frame:" , i)
    
    #get training image
    img2 = ps.grab(bbox)
    img2 = img2.convert('RGB')
    img2 = np.array(img2) 
    img2 = img2.astype(np.uint8)
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    # Find Key Points 2
    kp2, des2 = sift.detectAndCompute(img2,None)

    #Find Matches
    #FLANN_INDEX_KDTREE = 0
    #index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    #search_params = dict(checks = 4)
    flann = cv2.BFMatcher() #FlannBasedMatcher(index_params, search_params) #BFMatcher() #
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)


    #If good, find Homograpghy
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None


    #draw it all
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    if i == 0:
        frame = plt.imshow(img3, 'gray')
        plt.show()
    else:
        frame.set_data(img3)
        plt.draw()
        time.sleep(0.1)
