"""Create the report for the end to end pipeline"""

from dataclasses import dataclass
import os

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


class E2EReportManager:
    """Manage the report structure"""
    def __init__(self, report: Report) -> None:
        self.report = report

    def __call__(self) -> None:
        """Create the report"""
        self.create_report()
        return self

    def create_report(self) -> None:
        """Create the report"""
        self.create_file_paths(self.report)
        return self

    @staticmethod
    def create_file_paths(report: Report) -> None:
        """Create the file paths for the report"""
        if not os.path.exists(report.root_path):
            os.makedirs(report.root_path)
        if not os.path.exists(os.path.join(report.root_path, report.corrected_path)):
            os.makedirs(os.path.join(report.root_path, report.corrected_path))
        if not os.path.exists(os.path.join(report.root_path, report.mosaic_path)):
            os.makedirs(os.path.join(report.root_path, report.mosaic_path))
        if not os.path.exists(os.path.join(report.root_path, report.predicted_path)):
            os.makedirs(os.path.join(report.root_path, report.predicted_path))
        return True
