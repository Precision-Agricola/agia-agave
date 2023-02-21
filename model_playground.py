#%%
from skimage import io
from os.path import join 
import matplotlib.pyplot as plt


#read image in path 
path = join('DATA', 'rgb_12_pxl', 'sample.tif')
output_path = join('DATA', 'rgb_12_pxl', 'temp')
image = io.imread(path)


#create several images from the original one
columns = 4; rows = 2
height = image.shape[0]//rows
width = image.shape[1]//columns

for row in range(rows):
	for column in range(columns):
		image_crop = image[row*height:(row+1)*height, column*width:(column+1)*width]
		io.imsave(join(output_path, f'crop_{row}_{column}.png'), image_crop)