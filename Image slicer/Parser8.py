from .XmlDictParser import XmlDictParser
from .Parser8 import Parser8

parser = Parser8(XmlDictParser)
import glob
import xmltodict

from .MultipleFileAnnotationParser import MultipleFileAnnotationParser

class XmlDictParser(MultipleFileAnnotationParser):
    """Class that abstracts the annotation parsing of XML files using xmltodict library."""

    glob = "Annotations/**/*.xml"

    @classmethod
    def parse_file(cls, file, labels):
        """Parse an XML annotation file to a usable dict format."""
        with open(file, "r") as f:
            data = xmltodict.parse(f.read())
        name = data["annotation"]["filename"].split("/")[-1]
        slices = []
        labels = set()

        for obj in data["annotation"]["object"]:
            object_label = obj["name"]
            object_bndbox = obj["bndbox"]
            labels.add(object_label)
            slices.append({
                "xmin": round(float(object_bndbox["xmin"])),
                "ymin": round(float(object_bndbox["ymin"])),
                "xmax": round(float(object_bndbox["xmax"])),
                "ymax": round(float(object_bndbox["ymax"])),
                "label": object_label
            })

        return {"name": name, "slices": slices, "labels": labels}
