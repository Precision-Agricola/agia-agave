#%% import dense segmentation model (RestNet50 backbone)
from deepforest import main, get_data
from deepforest.main import deepforest
from wasabi import Printer
msg = Printer()

import os

class AgaveModel:
  def __init__(self):
    self.annotations_file = get_data(os.path.join(os.getcwd(),"DATA", "agave", "train.csv"))
    self.validation_file = get_data(os.path.join(os.getcwd(),"DATA", "agave", "test.csv"))
    self.save_dir = os.path.join(os.getcwd(),'pred_result')

  def model_init(self):
    return deepforest()
  
  def model_gpu_config(self, model):
    model.config['workers'] = 0 #use all the CPU resources [0]
    model.config['gpus'] = '-1' #move to GPU and use all the GPU resources
    model.config["train"]["csv_file"] = self.annotations_file
    model.config["train"]["root_dir"] = os.path.dirname(self.annotations_file)
    model.config["score_thresh"] = 0.5
    model.config["nms_thresh"] = 0.005
    model.config["train"]["lr"] = 0.0001
    model.config["train"]['epochs'] = 30
    model.config["validation"]["csv_file"] = self.validation_file
    model.config["validation"]["root_dir"] = os.path.dirname(self.validation_file)
    return model

  def model_trainer(self, model):
    model.create_trainer()
    model.use_release()
    return model

  def model_train(self, model):
    model.trainer.fit(model)
    return model
  
  def model_save_result(self, model):
    results = model.evaluate(
    self.annotations_file,
    os.path.dirname(self.annotations_file),
    iou_threshold = 0.4,
    savedir= self.save_dir
    )
    return results


def main():
    agave_model = AgaveModel()
    model = agave_model.model_init()
    model = agave_model.model_gpu_config(model)
    model = agave_model.model_trainer(model)
    model = agave_model.model_train(model)
    results = agave_model.model_save_result(model)
    msg.info(f"Model precision: {results['box_precision']}")
    msg.info(f"Model recall: {results['box_recall']}")
    return model


model = main()
#%% save the model with the today's date
import datetime
import os
import shutil

today = datetime.date.today()
model_path = os.path.join(os.getcwd(), "models", f"agave_{today}.h5")
model.save_model(model_path)

#%%
