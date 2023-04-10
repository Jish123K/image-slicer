import pandas as pd

from .SingleFileAnnotationParser import SingleFileAnnotationParser

class JSONParser(SingleFileAnnotationParser):
    """Class that abstracts the annotation parsing of the JSON format."""

    glob = "annotations/*.json"

    @classmethod
    def split_file(cls, file, labels):
        """Split a JSON annotation file into annotation items."""
        with open(file) as fp:
            data = json.load(fp)

        df_annotations = pd.DataFrame(data['annotations'])
        df_images = pd.DataFrame(data['images'])
        df_categories = pd.DataFrame(data['categories'])

        df_merged = pd.merge(df_annotations, df_images, how='left', left_on='image_id', right_on='id')
        df_merged = pd.merge(df_merged, df_categories, how='left', left_on='category_id', right_on='id')

        for image_id, df_image in df_merged.groupby('image_id'):
            name = df_image['file_name'].values[0].split("/")[-1]
            slices = []
            labels = set()

            for index, row in df_image.iterrows():
                if len(row['segmentation']) == 0:
                    object_label = row['name']
                    object_bndbox = row['bbox']
                    labels.add(object_label)
                    slices.append({
                        "xmin": round(object_bndbox[0]),
                        "ymin": round(object_bndbox[1]),
                        "xmax": round(object_bndbox[0] + object_bndbox[2]),
                        "ymax": round(object_bndbox[1] + object_bndbox[3]),
                        "label": object_label
                    })

            yield {"name": name, "slices": slices, "labels": labels}  
