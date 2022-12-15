""" Return the mateadata of the images in a list of images path"""

from core.sensor_utils import SensorUtils
from os.path import join
import micasense.metadata as metadata

def main():
    images_path = [
        join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_1.tif"),
        join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_2.tif"),	
        join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_3.tif"),
        join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_4.tif"),
        join("DATA", "pineapple", "SET000", "DATA", "IMG_0007_5.tif")
               ]
    bands_index = [
        "Red",
        "Green",
        "Blue",
        "NIR",
        "Red edge"
    ]
    meta = SensorUtils(images_path)
    meta()
    meta.meta.sort(key=lambda x: bands_index.index(x.get_item('XMP:BandName')))
    return meta


if __name__ == 'main':
    main()



	