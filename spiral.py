
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

def plot_spiral(r,img,parray,loops=8, makeGif=False):
	theta = 0
	imagelist = [img.convert(mode="RGB")];
	t = 0
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
		if t==0:
			r = [0]
		else:
			r = xrange(-t,t+1)
		for i in r:
			r = (init_radius)*theta + i 
			x = x_limit/2 + int(r*cos(theta))
			y = y_limit/2 + int(r*sin(theta))
			if x >0 and x < x_limit and y > 0 and y<y_limit and r>=thickness:
				img.putpixel((x,y),1)
				new_thickness=int(parray[x,y])
				if (new_thickness>t):
					t = t + 1;
				if (new_thickness<t):
					t = t - 1

				
	print count
	if makeGif:
		writeGif("result.gif",imagelist,duration=0.02,dither=0)
        
def get_photo_array(width,thickness):
    image = Image.open('moon2.jpg')
    ratio = float(image.size[1])/image.size[0]
    sizex = width
    sizey = int(round(ratio * sizex))
    pic = image.resize((sizex,sizey))
    r, g, b = pic.split()
    im = numpy.array(g)
    im = im/(256/(thickness*pi))
    im = numpy.around(im, decimals=0, out=None)
    photoarray = numpy.zeros([sizex,sizey])
    for num in range(0,numpy.size(im,1)):
                 for num2 in range(0,numpy.size(im,0)):
                    if int(im[num2,num])> 4:
                        photoarray[num][num2] = 4
                    else:
                        photoarray[num][num2] = int(im[num2,num])
                                 
    return photoarray

if __name__== '__main__':
	thickness = 2
	sequence = []
	photoarray = get_photo_array(2000,thickness)
	print photoarray.shape
	#numpy.set_printoptions(threshold=numpy.nan)
	IMAGE_SIZE = photoarray.shape
	img = Image.new('1',IMAGE_SIZE)
	plot_spiral(thickness,img,photoarray,50,False)
	smooth_photo(img)
	#img.save('test.png')
	print img.size

    

