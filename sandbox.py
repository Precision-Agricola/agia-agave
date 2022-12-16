#%%
from os.path import join
from skimage import io

images_path = [
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_1.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_2.tif"),	
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_3.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_4.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_5.tif")
			   ]

raw_images = []
for image_path in images_path:
	raw_images.append(io.imread(image_path))

#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os,glob
import math
import micasense.metadata as metadata

imageName = images_path[3]
meta = metadata.Metadata(imageName)

exiftoolPath = None
if os.name == 'nt':
    exiftoolPath = os.environ.get('exiftoolpath')
# get image metadata
meta = metadata.Metadata(imageName, exiftoolPath=exiftoolPath)

cameraMake = meta.get_item('EXIF:Make')
cameraModel = meta.get_item('EXIF:Model')
firmwareVersion = meta.get_item('EXIF:Software')
bandName = meta.get_item('XMP:BandName')

print('{0} {1} firmware version: {2}'.format(cameraMake, 
                                             cameraModel, 
                                             firmwareVersion))
print('Exposure Time: {0} seconds'.format(meta.get_item('EXIF:ExposureTime')))
print('Imager Gain: {0}'.format(meta.get_item('EXIF:ISOSpeed')/100.0))
print('Size: {0}x{1} pixels'.format(meta.get_item('EXIF:ImageWidth'),meta.get_item('EXIF:ImageHeight')))
print('Band Name: {0}'.format(bandName))
print('Center Wavelength: {0} nm'.format(meta.get_item('XMP:CentralWavelength')))
print('Bandwidth: {0} nm'.format(meta.get_item('XMP:WavelengthFWHM')))
print('Capture ID: {0}'.format(meta.get_item('XMP:CaptureId')))
print('Flight ID: {0}'.format(meta.get_item('XMP:FlightId')))
print('Focal Length: {0}'.format(meta.get_item('XMP:FocalLength')))


#%%
from core.sensor_utils import SensorUtils

set_path = images_path
meta = SensorUtils(set_path)
meta()

bands_index = [
	"Red",
	"Green",
	"Blue",
	"NIR",
	"Red edge"
]


#%% get the name file of the imageo
from micasense.utils import raw_image_to_radiance
radiance_images = []

for i, meta in enumerate(meta.meta):
	radiance_images.append(raw_image_to_radiance(meta, raw_images[i]))

proc_images = [image[0] for image in radiance_images]

#%%
from numpy import dstack
rgb_set = dstack((proc_images[2], proc_images[1], proc_images[0]))

plt.imshow(rgb_set)
#%% adjust the histogram
from skimage import exposure
p2, p98 = np.percentile(rgb_set, (2, 98))
img_rescale = exposure.rescale_intensity(rgb_set, in_range=(p2, p98))

plt.imshow(img_rescale)



#%%
from os.path import join
from core.sensor_utils import SensorUtils
images_path = [
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_1.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_2.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_3.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_4.tif"),
	join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_5.tif")]

sensor = SensorUtils(images_path).process_sensor()



#%% import matplotlib.pyplot as plt

#%%
from matplotlib import pyplot as plt
from skimage import io 
from os.path import join
panel_path = [] 
for i in range(1, 6):
	panel_path.append(join("DATA", "pineapple", "SET000", "PANEL", "IMG_0000_{}.tif".format(i)))

panel_images = []
for image_path in panel_path:
	panel_images.append(io.imread(image_path))

import cv2
import numpy as np

for i in range(0, 5):
	image = panel_images[i]
	image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
	ret, thresh = cv2.threshold(image, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	detections = []
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
		if len(approx) == 4:
			x, y, w, h = cv2.boundingRect(cnt)
			area = cv2.contourArea(cnt)
			ratio = float(w)/h
			if ratio > 0.95 and ratio < 1.05:
				if area > 0.00025*image.shape[0]*image.shape[1]:
					detections.append(cnt)
	bounding_boxes = []
	for cnt in detections:
		x, y, w, h = cv2.boundingRect(cnt)
		bounding_boxes.append((x, y, w, h))
	for box in bounding_boxes:
		x, y, w, h = box
		image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), 3)

	mean, std = [], []
	var = []
	for box in bounding_boxes:
		x, y, w, h = box
		image_region = image[x:w + x, y:h + y]
		mean.append(np.mean(image_region))
		std.append(np.std(image_region))
		var.append(np.var(image_region))

	from scipy import stats
	z = np.abs(stats.zscore(var))
	threshold =  1
	outliers = np.where(z > threshold)
	panel_region = bounding_boxes[outliers[0][0]]

	x, y, w, h = panel_region
	panel_region = image[y:y+h, x:x+w]
	print(z)

#%%
from os.path import join
from core.sensor_utils import PanelCalibration
panel_path = [] 
for i in range(1, 6):
	panel_path.append(join("DATA", "pineapple", "SET000", "PANEL", "IMG_0000_{}.tif".format(i)))

panel = PanelCalibration(panel_path).process_panel()

#%%
from matplotlib import pyplot as plt
plt.imshow(panel.panel_regions['blue'])