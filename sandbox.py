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

meta.meta.sort(key=lambda x: bands_index.index(x.get_item('XMP:BandName')))

#%% get the name file of the image
meta.meta[0]