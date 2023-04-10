import pandas as pd
from pathlib import Path

from .MultipleFileAnnotationParser import MultipleFileAnnotationParser

class Parser3(MultipleFileAnnotationParser):
    """Class that abstracts the annotation parsing of the Parser3 format."""

    glob = "*/label_2/**/*.txt"

    @classmethod
    def parse_file(cls, file, labels):
        """Parse a Parser3 annotation file to a usable dict format."""
        data = pd.read_csv(file, sep=" ", header=None, names=["type", "truncated", "occluded", "alpha", "bbox_left", "bbox_top", "bbox_right", "bbox_bottom", "dimensions_height", "dimensions_width", "dimensions_length", "location_x", "location_y", "location_z", "rotation_y", "score"])

        name = Path(file).stem
        slices = []
        labels = set()

        for _, obj in data.iterrows():
            object_label = obj["type"]
            labels.add(object_label)
            slices.append({
                "xmin": round(float(obj["bbox_left"])),
                "ymin": round(float(obj["bbox_top"])),
                "xmax": round(float(obj["bbox_right"])),
                "ymax": round(float(obj["bbox_bottom"])),
                "label": object_label
            })

        return {"name": name, "slices": slices, "labels": labels}
