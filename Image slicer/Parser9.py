import json
import os

class SingleFileAnnotationParser:
    """Base class that abstracts the annotation parsing in a single file."""

    file_path = ""
    """The path of the file to be parsed."""

    labels_file_path = ""
    """The path of the file with labels information."""

    @classmethod
    def parse_labels(cls, file):
        """Parse a labels file into a list of labels."""
        with open(cls.labels_file_path, "r") as f:
            return f.read().splitlines()

    @classmethod
    def split_file(cls, file, labels):
        """Split a specific annotation file into annotation items."""
        with open(cls.file_path, "r") as f:
            data = json.load(f)

        for item in data:
            slices = item["slices"]
            for slice in slices:
                label = labels[slice["label"]]
                yield {
                    "name": item["name"],
                    "slices": [{
                        "xmin": slice["xmin"],
                        "ymin": slice["ymin"],
                        "xmax": slice["xmax"],
                        "ymax": slice["ymax"],
                        "label": label
                    }],
                    "labels": labels
                }

    @classmethod
    def parse_item(cls, item):
        """Parse a specific annotation item to a usable dict format."""
        return item
