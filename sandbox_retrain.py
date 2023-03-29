""" This code shows the general steps to retrain a model using the deepforest package.
    The model can be loaded by creating a deepforest instance and then loading the state_dict."""

import torch
from deepforest import main, get_data
from deepforest.main import deepforest
from wasabi import Printer
import os
msg = Printer()

class AgaveModel:
  """This class is used to retrain the agave model."""
  def __init__(self):
    self.annotations_file = get_data(os.path.join(os.getcwd(),"DATA", "agave", "train.csv"))
    self.validation_file = get_data(os.path.join(os.getcwd(),"DATA", "agave", "test.csv"))
    self.save_dir = os.path.join(os.getcwd(),'pred_result')

  def model_init(self):
    """Initialize the model."""
    return deepforest()
  
  def model_gpu_config(self, model):
    """Configure the model to use GPU and the hyperparameters."""
    model.config['workers'] = 0 #use all the CPU resources [0]
    model.config['gpus'] = '-1' #move to GPU and use all the GPU resources
    model.config["train"]["csv_file"] = self.annotations_file
    model.config["train"]["root_dir"] = os.path.dirname(self.annotations_file)
    model.config["score_thresh"] = 0.1
    model.config["nms_thresh"] = 0.05
    model.config["train"]["lr"] = 0.0001
    model.config["train"]['epochs'] = 15
    model.config["validation"]["csv_file"] = self.validation_file
    model.config["validation"]["root_dir"] = os.path.dirname(self.validation_file)
    return model

  def model_trainer(self, model):
    """Create the trainer and use the release model."""
    model.create_trainer()
    model.use_release()
    return model

  def model_train(self, model):
    """Train the model."""
    model.trainer.fit(model)
    return model
  
  def model_save_result(self, model):
    """Save the model and evaluate the model."""
    if not os.path.exists(self.save_dir):
        os.makedirs(self.save_dir)
    results = model.evaluate(
    self.annotations_file,
    os.path.dirname(self.annotations_file),
    iou_threshold = 0.4,
    savedir= self.save_dir
    )
    model_name = "harvest_perception_bird_release.pt"
    model_path = os.path.join(self.save_dir, model_name)
    torch.save(model.state_dict(), model_path)
    return results

def main():
    """Main function."""
    agave_model = AgaveModel()
    model = agave_model.model_init()
    model = agave_model.model_gpu_config(model)
    model = agave_model.model_trainer(model)
    model = agave_model.model_train(model)
    results = agave_model.model_save_result(model)
    msg.info(f"Model precision: {results['box_precision']}")
    msg.info(f"Model recall: {results['box_recall']}")
    model.save()

if __name__ == "__main__":
    main()
