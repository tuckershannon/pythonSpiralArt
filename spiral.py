""" Module spiral.py
    
    This python program converts images into an Archimedes spiral type art made by varying
    the width of spiral as it travels away from the center

    Author: Tucker Shannon



"""



import numpy
from math import cos, sin, pi
from PIL import Image, ImageDraw, ImageSequence
from images2gif import writeGif
import cv2

def smooth_photo(img):
	smooth_img = numpy.array(img.convert(mode="RGB")); 
	smooth_img = cv2.blur(smooth_img,(3,3))
	cv2.imwrite("result.png",smooth_img)

def add_photo(img,imagelist):
	smooth_img = numpy.array(img.convert(mode="RGB")); 
	smooth_img = cv2.blur(smooth_img,(3,3))
	imagelist.append(smooth_img)

def plot_spiral(r,img,parray,loops=8, makeGif=False,background=0):
	theta = 0
	imagelist = Image.fromarray(img.astype('uint8'))
	t = 0
        maxInt = numpy.amax(parray)
	init_radius = r
	(x_limit,y_limit) = parray.shape
	count = 0
	while theta<2*pi*loops:
            if count == 720:
                    count = 0
                    if makeGif:
                            add_photo(img,imagelist)
            theta += float(1)/(2*r)
            count = count + 1
            for i in xrange(int(-t),int(t)+1):
                    r = (init_radius)*theta + i 
                    x = x_limit/2 + int(r*cos(theta))
                    y = y_limit/2 + int(r*sin(theta))
                    if x >0 and x < x_limit and y > 0 and y<y_limit:
                        if background == 1:
                            img[x][y] = [0,0,0]
                            new_thickness=maxInt-int(parray[x,y])
                        else: 
                            img[x][y] = [255,255,255]
                            new_thickness=(parray[x,y])
            if (new_thickness>t):
                t = t + .2;
            if (new_thickness<t):
                t = t - .2

				
	print count
	if makeGif:
		writeGif("result.gif",imagelist,duration=0.02,dither=0)
        
def get_photo_array(width,thickness,photoName):
    image = Image.open(photoName)
    ratio = float(image.size[1])/image.size[0]
    sizex = width
    sizey = int(round(ratio * sizex))
    pic = image.resize((sizex,sizey))
    r, g, b = pic.split()
    im = numpy.array(g)
    thickness = thickness*3
    im = im/(256/(thickness))
    im = numpy.around(im, decimals=0, out=None)
    photoarray = numpy.zeros([sizex,sizey])
    for num in range(0,numpy.size(im,1)):
                 for num2 in range(0,numpy.size(im,0)):
                    photoarray[num][num2] = int(im[num2,num])
                                 
    return photoarray

if __name__== '__main__':
	photoName = "tree.jpg" #name of photo to convert
        outputWidth = 2000 #how wide the output will be
        thickness = 3 #max thickness of spiral line
        background = 0; #0 for black 1 for white
    
	photoarray = get_photo_array(outputWidth,thickness,photoName)
	IMAGE_SIZE = photoarray.shape + (3,)
        
        if background == 1:
            img = numpy.full(IMAGE_SIZE,255)
        else:  
            img = numpy.full(IMAGE_SIZE,0)

        plot_spiral(thickness,img,photoarray,35,False,background)
        img = numpy.swapaxes(img,0,1)
	img = Image.fromarray(img.astype('uint8'))
        img.save('output.png')

    

