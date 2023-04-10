import cv2
import os

def slice_image(image_path, annotation_path, output_folder):
    # Load the image and annotation files
    image = cv2.imread(image_path)
    annotation = open(annotation_path, 'r').readlines()

    # Loop through the annotation file and extract each object
    for line in annotation:
        parts = line.strip().split(' ')
        x, y, w, h = map(int, parts[1:])
        object_img = image[y:y+h, x:x+w]

        # Save the object image to a file
        object_name = os.path.splitext(os.path.basename(image_path))[0] + '_' + parts[0] + '.jpg'
        object_path = os.path.join(output_folder, object_name)
        cv2.imwrite(object_path, object_img)

