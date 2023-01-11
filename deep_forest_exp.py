#%%
from deepforest import main 
from deepforest import get_data
import os 
import matplotlib.pyplot as plt

model = main.deepforest()
model.use_release()

img = model.predict_image(
	path = "temp_folder\image_correction.png",
 	return_plot = True
	)

plt.imshow(img[:,:,::-1])

#%%
