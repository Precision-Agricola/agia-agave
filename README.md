# Agia-agave

AI utilities and tools applied to precision agriculture. Status: experimentation and development of industrial applications (production estimation, plant counting, fruit detection, etc.) in agave, pineapple, and plantain plants.

## Project Manager

Alberto De Obeso

## Development Lead

[Precision Agricola](http://www.precisionagricola.com/)

# Development Plan

Currently

## AI PipeLine Setup

- Very Deep Convolutional Neural Networks _(N/A)_
- Pre-trained Models, re-train approach _(N/A)_
- Deep forest and documentation _(3 days)_

**Total days remaining: 3**

## Data Treatment

- Create Train/Test data _(2 weeks)_
- Data augmentation _(1-2 day)_
- Image acquisition _(N/A)_
- Image treatment _(N/A)_
    - Raw images 
    - Orthomosaic
- Image enhancement (Report delivery) _(N/A)_
- Post-Processing results _(3 days)_
    - Region Properties and stats


**Total days remainig: 2 weeks**

### Deep Forest and AI Experimentation and Implementation

- Agave Segmentation _(3 weeks)_,
- Agave Fusarium Identification _(1 week)_,
- Agave Phyllophaga Detection _(1 week)_
- Pineapple Fruit Detection _(2 weeks)_,

**Total days remainig: 2 months**
## Production 

- Consult client specifications
- Design developing plan (Analysis)
- Front-End dev
- Back-End dev
- Testing and maintenance

# Setup

Python 3.7 or newer is required and we have prepared a yml environment. First, install python from the [official web](https://www.python.org/) according to your operating system (currently Agia is not dockerized). Then activate and run the virtual enviroment, we recommend to use Anaconda. We recommend using Anaconda, although we also include the requirements file. Using Anaconda:

``` bash
conda env create -f src/agiaenv.yml
```

Or

``` bash
pip install -r src/requirements.txt
```

The models and training data are stored in a backblaze bucket. To sync data to the cloud, the backblaze must be accessed via the [CLI](https://www.backblaze.com/b2/docs/quick_command_line.html). Use the application credential to authorize the bucket interaction. Then you can download the model wanted, for example:

``` bash
b2 authorize-account
b2 download-file-by-name AgiaDev models/agave_2023-01-11.zip
```

Another way to synchronize the training data and the models is by running the script (the app id and the key are required):

``` bash
python data-sync.py
```
