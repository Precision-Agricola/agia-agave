#!/usr/bin/env python
# coding: utf-8
"""
Image processing utilities for multi-spectral agriculture images

Copyright 2021 Bitelemetric, S de R.L. de C.V.
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from pandas import read_excel
from pandas import DataFrame
from numpy import array, min, max, uint8, float32
from os import listdir, chdir, getcwd
from sys import path
from PIL import Image


# Normalize th values of an image
def normalizeImage(image, range = [0,255]):
    """Read an image array and normalized to a specif range of values

        Input: image(np.array). 
        Output: image(np.array[]).
    """

    minimum = min(image)
    maximum = max(image)

    # 0 - 1 image
    image_0_1 = (image - minimum) * 1 / (maximum - minimum)
    
    if max(range) == 255:
        return uint8(image_0_1 * (max(range) - min(range)) - min(range))
    else:
        return float32((image_0_1 * (max(range) - min(range))) + min(range))




# Transform multiple images in excel format to array format
def transformExcelToImage(files_path, supported_formats = [], range = [0,255]):

    """ Read an excel file that contains an image (similar to an array) and transform it to np.array


        Inputs: file_path (str). file.xlsx excel format.
                supported_formats (list[str]). list of the supported formats.
        Return: list of images (np.uint8 array). image normalized 0 to 255 (8-bites)."""

    if not supported_formats:
        supported_formats = ['xls',
                             'xlsx',
                             'xlsm',
                             'xlsb', 
                             'odf',
                             'ods']

    # Get all files in directory
    try:
        files = listdir(files_path)
    except:
        print('Error: no such file or dir: ' + str(files_path))
    

    # Filter supported files (excel files by default)
    excel_files = [files_path + '/' + file for file in files  if any(format in file for format in supported_formats)]
    
    # Validate files
    if not excel_files:
        print("Error: it seems that there are not supported files in the directory")
        return 0
    
    # Transform each excel image to an array image
    list_of_images= []

    for file in excel_files:
        image_row = DataFrame(read_excel(file))
        list_of_images.append(normalizeImage(image_row.to_numpy(), range = range))

    return list_of_images, excel_files


# Save a set of images
def saveImages(images, file_names, extension = '.png'):
    """Save a list of images in np.array format  

        Input:  images (list[np.array]). List of images
                result_path (str). Folder where the images will be stored
                extention (str)

    """


    # check if restult path provided
    if not file_names: file_names = getcwd()

    for name, image in zip(file_names, images):
        try:
            Image.fromarray(image).save(' '.join(name.split('.')[:-1]) + extension)
        except:
            print("Error saving the file in path" + ' '.join(name.split('.')[:-1]) + extensio )
            return False
    return True