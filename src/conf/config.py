from dataclasses import dataclass

@dataclass
class Paths:
	input_image: str
	mosaic_output: str
	labels: str
	train_file_name: str
	test_file_name: str

@dataclass
class Params:
	workers: int
	gpus: str
	score_thresh: float
	nms_thresh: float
	learning_rate: float
	epochs: int

@dataclass
class Preprocessing:
	rows: int
	columns: int

@dataclass
class DeepForestConfig:
	paths: Paths
	params: Params
	preprocessing: Preprocessing