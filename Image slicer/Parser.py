import xmltodict

from .SingleFileAnnotationParser import SingleFileAnnotationParser

class CVATImagesParser(SingleFileAnnotationParser):
    """Class that abstracts the annotation parsing of the CVAT for images format."""

    glob = "annotations.xml"

    @classmethod
    def split_file(cls, file, labels):
        """Split a CVAT for images annotation file into annotation items."""
        with open(file, 'r') as f:
            data = xmltodict.parse(f.read())

        for item in data['annotations']['image']:
            if 'box' in item:
                yield item

    @classmethod
    def parse_item(cls, item):
        """Parse a CVAT for images annotation item to a usable dict format."""
        name = item['@name'].split("/")[-1]
        slices = []
        labels = set()

        for obj in item['box']:
            object_label = obj['@label']
            labels.add(object_label)
            slices.append({
                "xmin": round(float(obj['@xtl'])),
                "ymin": round(float(obj['@ytl'])),
                "xmax": round(float(obj['@xbr'])),
                "ymax": round(float(obj['@ybr'])),
                "label": object_label
            })

        return {"name": name, "slices": slices, "labels": labels}  
