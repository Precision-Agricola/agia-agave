"""E2E pipeline"""

from dataclasses import dataclass
from os.path import join
from skimage import io
from e2e_report import E2EReportManager
from image_processor import E2EImageProcessor
from core.image_utils import ImageUtils


@dataclass
class Inputs:
    """Input paths"""
    sensor_set:str
    panel_set:str

@dataclass
class Report:
    """Report output dataclass"""
    root_path: str
    corrected_path: str
    mosaic_path: str
    predicted_path: str

@dataclass
class SensorSet:
    """Sensor set dataclass"""
    data_set: list[str]
    panel_set: list[str]

class Pipeline:
    """E2E pipeline"""

    def __init__(self, inputs: Inputs, report: Report, sensor: SensorSet) -> None:
        self.inputs = inputs
        self.report = report
        self.sensor = sensor
        self.rgb = None
        self.mosaic = []

    def run(self) -> None:
        """Run the pipeline"""
        self.create_report_template()
        self.image_preprocessing()
        self.image_mosaic()
        self.image_prediction()
        return self

    def create_report_template(self) -> None:
        """Create the report template"""
        manager = E2EReportManager(self.report)
        manager.create_report()
        return self

    def image_preprocessing(self) -> None:
        """Image preprocessing"""
        processor = E2EImageProcessor(self.sensor)
        images = processor.image_preprocessing()
        rgb = images.rgb
        io.imsave(join(self.report.root_path,self.report.corrected_path,"rgb.png"), rgb)
        self.rgb = rgb
        return self

    def image_mosaic(self) -> None:
        """Image mosaic"""
        rows = 4
        columns = 5
        image_utils = ImageUtils
        for row in range(1, rows + 1):
             for column in range(1, columns + 1):
                try:
                    image = image_utils.get_sample_by_matrix(
                        self.rgb, (rows, columns), (row, column)
                    )
                    self.mosaic.append(image)
                    io.imsave(join(self.report.root_path,self.report.mosaic_path,f"mosaic_{row}_{column}.png"), image)
                except:
                    image = image_utils.get_sample_by_matrix(
                        self.rgb, (rows, columns), (row, column)
                    )
                    self.mosaic.append(image)
                    io.imsave(join(self.report.root_path,self.report.mosaic_path,f"mosaic_{row}_{column}.png"), image)
        return self

    def image_prediction(self) -> None:
        """Image prediction"""
        return self

def main() -> None:
    """Main function"""
    inputs = Inputs(
        sensor_set="sensor_set",
        panel_set="panel_set"
    )
    report = Report(
        root_path="temp_folder",
        corrected_path="corrected",
        mosaic_path="mosaic",
        predicted_path="predicted"
    )
    sensor = SensorSet(
        data_set=join("DATA", "agave", "SET000", "DATA"),
        panel_set=join("DATA", "agave", "SET000", "PANEL")
    )
    pipeline = Pipeline(inputs, report, sensor)
    pipeline.run()

if __name__ == "__main__":
    main()
