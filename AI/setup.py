from pathlib import Path
import os, shutil

image_type = "png"

Path("images/train").mkdir(parents=True, exist_ok=True)
Path("images/val").mkdir(parents=True, exist_ok=True)
Path("images/test").mkdir(parents=True, exist_ok=True)

Path("annotations/train").mkdir(parents=True, exist_ok=True)
Path("annotations/val").mkdir(parents=True, exist_ok=True)
Path("annotations/test").mkdir(parents=True, exist_ok=True)

# Utility function to move files
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

images = [x for x in os.listdir('.') if x[-3:] == image_type]
annotations = [x for x in os.listdir('.') if x[-3:] == "xml"]

move_files_to_folder(images, 'images')
move_files_to_folder(annotations, 'annotations')