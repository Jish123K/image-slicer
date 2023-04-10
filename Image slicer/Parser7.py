import pandas as pd
from .Parser7 import Parser7

class AlternativeParser(Parser7):
    """Class that abstracts the annotation parsing of the Open Images format using pandas."""

    glob = "annotations/*-annotations-bbox.csv"

    @classmethod
    def split_file(cls, file, labels):
        """Split an Open Images annotation file into annotation items."""
        data = pd.read_csv(file)

        for name, group in data.groupby("ImageID"):
            slices = []

            for _, row in group.iterrows():
                slices.append({
                    "xmin": row["XMin"],
                    "ymin": row["YMin"],
                    "xmax": row["XMax"],
                    "ymax": row["YMax"],
                    "label": row["LabelName"]
                })

                labels.add(row["LabelName"])

            yield {"name": name.split("/")[-1], "slices": slices, "labels": labels}

    @classmethod
    def parse_item(cls, item):
        """Parse an Open Images annotation item to a usable dict format."""
        return item
