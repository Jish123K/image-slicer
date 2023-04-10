from pathlib import Path
import pandas as pd

from .MultipleFileAnnotationParser import MultipleFileAnnotationParser

class Parser11(MultipleFileAnnotationParser):
    """Class that abstracts the annotation parsing using pandas library."""

    glob = "obj_*_data/**/*.txt"
    labels = "obj.names"

    @classmethod
    def parse_labels(cls, file):
        with open(file) as fp:
            labels = fp.readlines()

        return [label.strip() for label in labels]

    @classmethod
    def parse_file(cls, file, labels_list):
        """Parse a annotation file to a usable dict format using pandas."""

        file_path = Path(file)
        name = file_path.stem
        data = pd.read_csv(file_path, header=None, names=["label_id", "cx", "cy", "rw", "rh"], delimiter=" ")
        data["label"] = data["label_id"].apply(lambda x: labels_list[x])

        slices = data.apply(lambda row: {
            "xmin": row.cx - (row.rw/2),
            "ymin": row.cy - (row.rh/2),
            "xmax": row.cx + (row.rw/2),
            "ymax": row.cy + (row.rh/2),
            "label": row.label
        }, axis=1).tolist()

        return {"name": name, "slices": slices, "labels": set(labels_list)}
