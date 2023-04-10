from pathlib import Path
import json

class Parser5:
    """Base class that abstracts the annotation parsing in multiple files."""

    def __init__(self, glob_pattern, labels_file):
        """Initialize the parser with glob pattern and labels file."""
        self.glob_pattern = glob_pattern
        self.labels_file = labels_file
        self.labels = self.parse_labels(labels_file)

    def parse_labels(self, file):
        """Parse a labels file into a list of labels."""
        with open(file) as f:
            labels = json.load(f)
        return labels

    def parse_file(self, file):
        """Parse a specific annotation file to a usable dict format."""
        with open(file) as f:
            data = json.load(f)
        name = Path(file).stem
        slices = data["slices"]
        labels = {label: idx for idx, label in enumerate(self.labels)}
        parsed_data = {"name": name, "slices": [], "labels": labels}
        for slice_data in slices:
            xmin = slice_data["xmin"]
            ymin = slice_data["ymin"]
            xmax = slice_data["xmax"]
            ymax = slice_data["ymax"]
            label = slice_data["label"]
            parsed_data["slices"].append({
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax,
                "label": label
            })
        return parsed_data
