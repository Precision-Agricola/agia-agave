""" Run the deep forest model retrain process end to end. """
#%%
from core.train import TrainUtils
from core.train import Trainer, Paths
from os.path import join

# define the input and output paths
input_path = join('DATA', 'rgb_12_pxl', 'sample.tif')
output_path = join('DATA', 'rgb_12_pxl', 'mosaic')
train_folder = join('DATA', 'rgb_12_pxl', 'train', 'labels')
trainer = Trainer(
	paths=Paths(
		input_image=input_path,
		output=output_path,
		labels=train_folder
	)
)

# create the training mosaic
trainer = TrainUtils(trainer)
trainer.create_train_mosaic(3, 3)

# then create the csv file with the labels. once the mosaic is created, manually label the images
trainer.create_train_csv()



