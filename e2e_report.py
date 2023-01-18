"""Create the report for the end to end pipeline"""

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
import os

@dataclass
class E2EReport:
    """Report dataclass"""
    root_path: str
    corrected_path: str
    mosaic_path: str
    predicted_path: str
    report_id: str

class E2EReportManager:
    """Manage the report structure"""
    def __init__(self, report: E2EReport) -> None:
        self.report = report

    def __call__(self) -> None:
        """Create the report"""
        self.create_report()

    def create_report(self) -> None:
        """Create the report"""
        self.create_file_paths(self.report)

    @staticmethod
    def create_file_paths(report: E2EReport) -> None:
        """Create the file paths for the report"""
        values = report.__dict__.values()
        paths = [path for path in values if path not in [report.root_path, report.report_id]]
        for path in paths:
            os.makedirs(os.path.join(report.root_path, path), exist_ok=True)
            with open(os.path.join(report.root_path, path, ".gitkeep"), "w", encoding="utf8") as f:
                f.write("")
        return paths

def main():
    """Main function"""
    time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    report = E2EReport(
        report_id=str(uuid4())+"_"+time,
        root_path="temp_folder",
        corrected_path="corrected",
        mosaic_path="mosaic",
        predicted_path="predicted_path"
    )
    e2e_report_manager = E2EReportManager(report)
    e2e_report_manager()

if __name__ == "__main__":
    main()
