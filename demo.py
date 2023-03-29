""" Run the deep forest model retrain process end to end. """
#%%
from core.train import TrainUtils
from src.conf.config import DeepForestConfig
from hydra.core.config_store import ConfigStore
from wasabi import Printer
import hydra
from skimage import io
msg = Printer()

config_store = ConfigStore.instance()
config_store.store(name="deep_forest_config", node=DeepForestConfig)

@hydra.main(config_path= "src/conf", config_name="config_gpu", version_base="1.1")
def main(config: DeepForestConfig): 
    """ Main function to run the deep forest model retrain process end to end."""

    trainer = TrainUtils(config)
    trainer.create_train_mosaic(
        columns=config.preprocessing.columns,
        rows=config.preprocessing.rows,
    )
    trainer.create_train_csv(
        train_file_name=config.paths.train_file_name,
    )
    model = trainer.train()
    model.trainer.fit(model)
    image = model.predict_image(
        path=config.paths.test_file_name,
        return_plot=True
        )
    io.imsave(config.paths.test_file_name.replace('png','tif'), image[:,:,::-1])
    return model

if __name__ == "__main__":
    main()

#%%
model = main()

#%%
print('hello world')