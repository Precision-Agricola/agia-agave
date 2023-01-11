#%%
import cv2
import pandas as pd
from os import listdir
from os.path import join
from skimage import io
import numpy as np
from matplotlib import pyplot as plt

ground_truth_path = join("DATA", "agave", "ground_truth")
ground_truth_files = [join(ground_truth_path, f) for f in listdir(ground_truth_path)]
ground_truth_images = [io.imread(f) for f in ground_truth_files]

reference_path = join("DATA", "agave", "reference")
reference_files = [join(reference_path, f) for f in listdir(reference_path)]

value_fixed_images = [np.where(img > 0, 255, 0) for img in ground_truth_images]
value_fixed_images = [img.astype(np.uint8) for img in value_fixed_images]

training_percent = 0.75
testing_percent = 0.25
training_size = int(len(value_fixed_images) * training_percent)
testing_size = int(len(value_fixed_images) * testing_percent)
training_images = value_fixed_images[:training_size]
testing_images = value_fixed_images[training_size:]

output_train_path = join("DATA", "agave", "train")
for i, img in enumerate(training_images):
	io.imsave(join(output_train_path, f"train_{i}.png"), img)
output_test_path = join("DATA", "agave", "test")
for i, img in enumerate(testing_images):
	io.imsave(join(output_test_path, f"test_{i}.png"), img)


data_frame = pd.DataFrame(columns=["image_path", "xmin", "ymin", "xmax", "ymax", "label"])

for i, img in enumerate(training_images):
	image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
	_, thresh = cv2.threshold(image, 127, 255, 0)
	contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		box = cv2.boundingRect(cnt)
		height, width = box[3], box[2]
		left, top = box[0], box[1]
		data_frame = data_frame.append({
			"image_path":reference_files[i],
			"xmin":left,
			"ymin":top,
			"xmax":left+width,
			"ymax":top+height,
			"label":"Tree"
		}, ignore_index=True)

data_frame.to_csv(join("DATA", "agave", "train.csv"), index=False)

test_data_frame = pd.DataFrame(columns=["image_path", "xmin", "ymin", "xmax", "ymax", "label"])
for i, img in enumerate(testing_images):
	image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
	_, thresh = cv2.threshold(image, 127, 255, 0)
	contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		box = cv2.boundingRect(cnt)
		height, width = box[3], box[2]
		left, top = box[0], box[1]
		test_data_frame = test_data_frame.append({
			"image_path":reference_files[i + training_size],
			"xmin":left,
			"ymin":top,
			"xmax":left+width,
			"ymax":top+height,
			"label":"Tree"
		}, ignore_index=True)
test_data_frame.to_csv(join("DATA", "agave", "test.csv"), index=False)
#%%
