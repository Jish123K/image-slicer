from .Parser10 import Parser10

parser = Parser10()
import pandas as pd
from pathlib import Path
from .SingleFileAnnotationParser import SingleFileAnnotationParser

class Parser10(SingleFileAnnotationParser):
    """Class that abstracts the annotation parsing of the Parser10 format."""

    glob = "parser10_annotations/*.txt"

    @classmethod
    def split_file(cls, file, labels):
        """Split a Parser10 annotation file into annotation items."""
        df = pd.read_csv(file, sep='\t')
        grouped = df.groupby('filename')
        for filename, group in grouped:
            slices = []
            labels = set()
            for index, row in group.iterrows():
                object_label = row['class']
                labels.add(object_label)
                xmin = round(row['xmin'])
                ymin = round(row['ymin'])
                xmax = round(row['xmax'])
                ymax = round(row['ymax'])
                slices.append({
                    "xmin": xmin,
                    "ymin": ymin,
                    "xmax": xmax,
                    "ymax": ymax,
                    "label": object_label
                })
            yield {"name": filename, "slices": slices, "labels": labels}

    @classmethod
    def parse_item(cls, item):
        """Parse a Parser10 annotation item to a usable dict format."""
        name = item["name"]
        slices = item["slices"]
        labels = item["labels"]
        return {"name": name, "slices": slices, "labels": labels}
