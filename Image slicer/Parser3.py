import json
from pathlib import Path

from .SingleFileAnnotationParser import SingleFileAnnotationParser

class DatumaroParser(SingleFileAnnotationParser):
    """Class that abstracts the annotation parsing of the Datumaro format."""

    glob = "annotations/*.json"

    @classmethod
    def split_file(cls, file, labels):
        """Split a Datumaro annotation file into annotation items."""
        with open(file) as fp:
            data = json.load(fp)

        labels = [label.get("name") for label in data.get("categories").get("label").get("labels")]

        return [
            item
            for item in data.get("items")
            if any(annotation.get("type") == "bbox" for annotation in item.get("annotations"))
        ]

    @classmethod
    def parse_item(cls, item):
        """Parse a Datumaro annotation item to a usable dict format."""
        name = Path(item.get("id")).stem
        slices = []
        labels = set()

        for obj in item.get("annotations"):
            if obj.get("type") == "bbox":
                object_label = obj.get("label_id")
                object_bndbox = obj.get("bbox")
                labels.add(object_label)
                slices.append({
                    "xmin": round(object_bndbox[0]),
                    "ymin": round(object_bndbox[1]),
                    "xmax": round(object_bndbox[0] + object_bndbox[2]),
                    "ymax": round(object_bndbox[1] + object_bndbox[3]),
                    "label": object_label
                })

        return {"name": name, "slices": slices, "labels": labels}
