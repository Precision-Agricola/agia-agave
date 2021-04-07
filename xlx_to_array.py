"""
Take th
"""
#%%
# Load agia library
import agia
from time import time
from numpy import min, max


# Transform excel images to np array
def main():

    # Transform excel images to np array
    transform_time = time()

    images, file_names = agia.transformExcelToImage(files_path = 'SAMPLE_DATA', range=[0, 255])

    print("Procesing excel to arrat image time", str(time() - transform_time))
    print("*** Data type and range ***")
    print("Images class:", type(images[0]))
    print("Images range: ", min(images[0]), max(images[0]))


    # Store the info 
    agia.saveImages(images, file_names, extension = '.png')
        
        

if __name__ == '__main__':
    main()
