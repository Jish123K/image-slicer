import xmltodict
from .MultipleFileAnnotationParser import MultipleFileAnnotationParser

class Parser4(MultipleFileAnnotationParser):
    """Class that abstracts the annotation parsing of the LabelMe format."""

    glob = "*/**/*.xml"

    @classmethod
    def parse_file(cls, file, labels):
        """Parse a LabelMe annotation file to a usable dict format."""
        with open(file) as f:
            data = xmltodict.parse(f.read())

        name = data["annotation"]["filename"]
        slices = []
        labels = set()

        for obj in data["annotation"]["object"]:
            object_type = obj.get("type")

            if object_type is not None and object_type == "bounding_box":
                object_label = obj["name"]
                object_bndbox = obj["polygon"]
                object_points = object_bndbox["pt"]
                labels.add(object_label)
                slices.append({
                    "xmin": round(float(object_points[0]["x"])),
                    "ymin": round(float(object_points[0]["y"])),
                    "xmax": round(float(object_points[2]["x"])),
                    "ymax": round(float(object_points[2]["y"])),
                    "label": object_label
                })

        return {"name": name, "slices": slices, "labels": labels}
