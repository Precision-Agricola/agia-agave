#%%
from core.image_utils import ImageUtils
from os.path import join 
import matplotlib.pyplot as plt

images_path = [
	join('data', 'pineapple_ortho', '1.tif'),
	join('data', 'pineapple_ortho', '2.tif'),
	join('data', 'pineapple_ortho', '3.tif'),
	join('data', 'pineapple_ortho', '4.tif'),
	join('data', 'pineapple_ortho', '5.tif')
	]

images = ImageUtils.read_images_from_path(images_path)
matrix_data = ImageUtils.get_slices_params(images[0], 20, 8)
slice = ImageUtils.get_slice_by_matrix(images[0], matrix_data[0], matrix_data[1])
plt.imshow(slice, cmap='gray')