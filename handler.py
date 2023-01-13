from core.image_utils import ImageUtils
from os.path import join 
from numpy import dstack
from skimage import exposure, io

class SegmentHandler(ImageUtils):
    def __init__(self, images_path, method, params):
        self.images_path = images_path
        self.method = method
        self.params = params

    def __call__(self):
        self.images = self.read_images_from_path(self.images_path)
        self.samples = self.get_samples(method=self.method, params=self.params)
        self.rgb_image = self.get_rgb()
        return self

    def get_samples(self, method, params):
        """Get samples from the images."""
        samples = []
        if method == "list":
            for image in self.images:
                samples.append(self.get_sample_by_list(image, params["slices_no"], params["sample_index"]))
        elif method == "matrix":
            for image in self.images:
                samples.append(self.get_sample_by_matrix(image, params["matrix_size"], params["slice_tuple"]))
        else:
            raise ValueError("Invalid method")
        return samples

    def get_rgb(self):
        """Get RGB image from a list of images."""
        rgb = dstack(self.samples[:3])
        return exposure.rescale_intensity(rgb, out_range=(0, 255)).astype("uint8")

def main():
    images_path = [
        join('data', 'pineapple_ortho', '1.tif'),
        join('data', 'pineapple_ortho', '2.tif'),
        join('data', 'pineapple_ortho', '3.tif'),
        join('data', 'pineapple_ortho', '4.tif'),
        join('data', 'pineapple_ortho', '5.tif')
        ]
    method = "matrix"
    params = {"matrix_size": (40, 30), "slice_tuple": (20, 15)}
    samples = SegmentHandler(images_path, method, params)
    samples()
    io.imsave('temp_folder/sample_rgb.tif', samples.rgb_image)
    return samples

if __name__ == '__main__':
    main()