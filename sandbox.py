"""Sand box for image correction utils"""
#%%
from os.path import join
from core.red_edge_sensor import Panel, Sensor, ImageProcessor
from numpy import dstack

def main():
    panel_set_path = []
    sensor_set_path = []
    for i in range(1, 6):
        panel_set_path.append(join("DATA", "agave","PANEL", "IMG_0001_{}.tif".format(i)))
        sensor_set_path.append(join("DATA", "agave", "DATA", "IMG_0007_{}.tif".format(i)))
    panel = Panel(set_path=panel_set_path)
    sensor = Sensor(set_path=sensor_set_path)
    image_processed = ImageProcessor(panel=panel, sensor=sensor)
    rgb_set = dstack((
        image_processed.adjusted_images['red'],
        image_processed.adjusted_images['green'],
        image_processed.adjusted_images['blue']))
    from skimage import io
    io.imsave("temp_folder/image_correction.png", rgb_set)
    return image_processed.adjusted_images

if __name__ == "__main__":
    images = main()
