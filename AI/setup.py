import argparse
import torch
from IPython.display import Image  # for displaying images
import os 
import random
import shutil
import csv
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

random.seed(20439472)

def parse_opt(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-directory", type=str, default="images")
    parser.add_argument("-a", "--annotations-directory", type=str, default="annotations")
    parser.add_argument("-t", "--image-type", type=str, default="png")
    parser.add_argument("-c", "--classes-file", type=str, default="classes.txt")
    parser.add_argument("-o", "--output-directory", type=str, default="")
    return parser.parse_args(args)

# Reads classes from csv file
def read_classes(csv_file):
    with open(csv_file, newline='') as file:
        data = list(csv.reader(file))

    classes = {}
    for i in range(len(data)):
        classes[data[i]] = i
    return classes

# Function to get the data from XML Annotation
def extract_info_from_xml(xml_file):
    root = ET.parse(xml_file).getroot()
    
    # Initialise the info dict 
    info_dict = {}
    info_dict['bboxes'] = []

    # Parse the XML Tree
    for elem in root:
        # Get the file name 
        if elem.tag == "filename":
            info_dict['filename'] = elem.text
            
        # Get the image size
        elif elem.tag == "size":
            image_size = []
            for subelem in elem:
                image_size.append(int(subelem.text))
            
            info_dict['image_size'] = tuple(image_size)
        
        # Get details of the bounding box 
        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                    
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)            
            info_dict['bboxes'].append(bbox)
    
    return info_dict

# Convert the info dict to the required yolo format and write it to disk
def convert_to_yolov5(info_dict):
    print_buffer = []
    
    # For each bounding box
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
        
        # Transform the bbox co-ordinates as per the format required by YOLO v5
        b_center_x = (b["xmin"] + b["xmax"]) / 2 
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width    = (b["xmax"] - b["xmin"])
        b_height   = (b["ymax"] - b["ymin"])
        
        # Normalise the co-ordinates by the dimensions of the image
        image_w, image_h, image_c = info_dict["image_size"]  
        b_center_x /= image_w 
        b_center_y /= image_h 
        b_width    /= image_w 
        b_height   /= image_h 
        
        #Write the bbox details to the file 
        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
        
    # Name of the file which we have to save 
    save_file_name = os.path.join(args.output_directory, "labels", info_dict["filename"].replace("png", "txt"))
    
    # Save the annotation to disk
    print("\n".join(print_buffer), file=open(save_file_name, "w"))

# Utility function to make a folder
def make_folder(path1, path2=''):
    path = os.path.join(path1, path2)
    os.makedirs(path, exist_ok=True)

# Utility function to move files
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

args = parse_opt(sys.argv[1:])
print(args.images_directory)
print(args.annotations_directory)
print(args.base_directory)
print(args.classes_file)
print(args.image_type)

"""
images = [x for x in os.listdir(args.images_directory) if x[-3:] == image_type]
annotations = [x for x in os.listdir(args.annotations_directory) if x[-3:] == "xml"]

move_files_to_folder(images, 'images')
move_files_to_folder(annotations, 'annotations')
"""

# Get the annotations
annotations = [os.path.join(args.annotations_directory, x) for x in os.listdir(args.annotations_directory) if x[-3:] == "xml"]
annotations.sort()

# Convert and save the annotations as labels
for ann in tqdm(annotations):
    info_dict = extract_info_from_xml(ann)
    convert_to_yolov5(info_dict)

# Read images and labels
images = [os.path.join(args.images_directory, x) for x in os.listdir(args.images_directory) if x[-3:] == image_type]
labels_dir = os.path.join(args.output_directory, "labels")
labels = [os.path.join(labels_dir, x) for x in os.listdir(labels_dir) if x[-3:] == "txt"]

images.sort()
labels.sort()

# Split the dataset into train-validate splits 
train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size = 0.2, random_state = 1)

# Make the train and validate folders
make_folder(args.output_directory, "images/train")
make_folder(args.output_directory, "images/val")

make_folder(args.output_directory, "labels/train")
make_folder(args.output_directory, "labels/val")

# Move the splits into their folders
move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val')
move_files_to_folder(train_annotations, 'labels/train')
move_files_to_folder(val_annotations, 'labels/val')