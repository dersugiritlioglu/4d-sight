import cv2
import os
import ipdb
import numpy as np
import math
from scipy import ndimage
from scipy.spatial.distance import euclidean
from math import *
import imutils

imagepath = 'E:/Users/lenovo/Desktop/4d_sight'
imnames = ['Small_area.png',
			'Small_area_rotated.png',
			'StarMap.png']

def read_image(imagepath):
	img = cv2.imread(imagepath)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	return img

def find_aligned(big,small):
	for x in range(big.shape[0]-small.shape[0]+1):
		for y in range(big.shape[1]-small.shape[1]+1):
			if np.array_equal(small, big[x:small.shape[0]+x, y:small.shape[1]+y]):
				ul = (x,y)
				ur = (x+small.shape[0],y)
				ll = (x,y+small.shape[1])
				lr = (x+small.shape[0],y+small.shape[1])
				return ul,ur,ll,lr
	return -1,-1,-1,-1

def get_idx(array, number):
	idx1_x, idx1_y = np.where(array==number)
	idxs = []
	for i in range(len(idx1_x)):
		idxs.append((idx1_x[i],idx1_y[i]))

	return idxs

starmap = read_image(os.path.join(imagepath, imnames[2]))
starmap_gray = np.mean(starmap,axis=2)
small_r = read_image(os.path.join(imagepath, imnames[1]))
small_r_gray = np.mean(small_r,axis=2)

# since there are white pixels around borders, coming from rotation (just in case)
crop = 2
smaller_r = small_r[crop:-crop,crop:-crop] 
smaller_r_gray = small_r_gray[crop:-crop,crop:-crop]
small = read_image(os.path.join(imagepath, imnames[0]))

# For the rotated image (IT DOESN'T WORK YET)
flat = smaller_r_gray.flatten()
flat.sort()
max1 = flat[-1]
max2 = flat[-101]

idx1=get_idx(smaller_r_gray,max1)
idx2=get_idx(smaller_r_gray,max2)
big_idx1=get_idx(starmap_gray,max1)
big_idx2=get_idx(starmap_gray,max2)


distance_in_small = euclidean(idx1[0],idx2[0])
same_distances = []
for i in big_idx1:
	for j in big_idx2:
		if np.abs(round(euclidean(i,j))-round(distance_in_small))<=10:
			same_distances.append((i,j))

angles = []
for P1,P2 in same_distances:
	P1_x,P1_y = P1
	P2_x,P2_y = P2
	deltaY = P2_y - P1_y
	deltaX = P2_x - P1_x
	angles.append(atan2(deltaY, deltaX) * 180 / pi)

rotated = []
for angle in angles:
	rotated.append(imutils.rotate(smaller_r_gray, angle=angle))

for point in same_distances:
	x_org, y_org = smaller_r_gray.shape[0],smaller_r_gray.shape[1]
	starmap_crop = starmap_gray[point[0][0]-x_org:point[0][0]+x_org,point[0][1]-y_org:point[0][1]+y_org]
	ul2,ur2,ll2,lr2=find_aligned(starmap_crop,small_r_gray)
	print(point)
	ipdb.set_trace()
	if (ul1,ur1,ll1,lr1) != (-1,-1,-1,-1):
		print("Found! Around ", point) 

############################################################################################################

# For the non-rotated image
ul1,ur1,ll1,lr1 = find_aligned(starmap,small)

# This is commented out since the aligned function would not solve this image
# It would return -1 for all variables.
# ul2,ur2,ll2,lr2 = find_aligned(starmap,small_r)

with open('small_corners.txt','w') as file:
	file.write(str(ul1)+" "+str(ur1)+" "+str(ll1)+" "+str(lr1))
with open('small_rotated_corners.txt','w') as file:
	file.write(str(ul2)+" "+str(ur2)+" "+str(ll2)+" "+str(lr2))





