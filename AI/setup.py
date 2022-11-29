import sys, argparse
import torch
from IPython.display import Image  # for displaying images
import os 
import random
import shutil
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def parse_opt(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-directory", type=str, default="images")
    parser.add_argument("-a", "--annotations-directory", type=str, default="annotations")
    parser.add_argument("-t", "--image-type", type=str, default="png")
    parser.add_argument("-c", "--classes-file", type=str, default="classes.txt")
    parser.add_argument("-o", "--output-directory", type=str, default="")
    parser.add_argument("-d", "--yolov5-directory", type=str, default="yolov5")
    parser.add_argument("-n", "--yaml-file-name", type=str, default="data.yaml")
    return parser.parse_args(args)

args = parse_opt(sys.argv[1:])
random.seed(20439472)

# Reads classes from classes file
def read_classes(classes_file):
    with open(classes_file) as file:
        classes = [line.rstrip() for line in file]
    
    classes_by_id = {}
    for i in range(len(classes)):
        classes_by_id[classes[i]] = i
    return classes, classes_by_id

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
            class_id = classes_by_id[b["class"]]
        except KeyError:
            print("Invalid Class. Must be one from ", classes_by_id.keys())
        
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
    save_file_name = os.path.join(args.output_directory, "labels", info_dict["filename"][0:-3] + "txt")
    
    # Save the annotation to disk
    print("\n".join(print_buffer), file=open(save_file_name, "w"))

def write_yaml(file_name):    
    images_path = os.path.relpath(args.images_directory, args.yolov5_directory)
    
    train_path = "train: " + os.path.join(images_path, "train")
    val_path = "val: " + os.path.join(images_path, "val")
    test_path = "test: "
    
    num_classes = "nc: " + str(len(classes))
    class_names = "names: " + str(classes)
    
    print_buffer = []
    print_buffer.append(train_path)
    print_buffer.append(val_path)
    print_buffer.append(test_path)
    print_buffer.append("")
    print_buffer.append(num_classes)
    print_buffer.append(class_names)
    
    print("\n".join(print_buffer), file=open(file_name, "w"))

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

"""
images = [x for x in os.listdir(args.images_directory) if x[-3:] == image_type]
annotations = [x for x in os.listdir(args.annotations_directory) if x[-3:] == "xml"]

move_files_to_folder(images, 'images')
move_files_to_folder(annotations, 'annotations')
"""

classes, classes_by_id = read_classes(args.classes_file)

# Get the annotations
annotations = [os.path.join(args.annotations_directory, x) for x in os.listdir(args.annotations_directory) if x[-3:] == "xml"]
annotations.sort()

# Make the train and validate folders
make_folder(args.output_directory, "images/train")
make_folder(args.output_directory, "images/val")

make_folder(args.output_directory, "labels/train")
make_folder(args.output_directory, "labels/val")

# Convert and save the annotations as labels
for ann in tqdm(annotations):
    info_dict = extract_info_from_xml(ann)
    convert_to_yolov5(info_dict)
#exit()

# Read images and labels
images = [os.path.join(args.images_directory, x) for x in os.listdir(args.images_directory) if x[-3:] == args.image_type]
labels_dir = os.path.join(args.output_directory, "labels")
labels = [os.path.join(labels_dir, x) for x in os.listdir(labels_dir) if x[-3:] == "txt"]

images.sort()
labels.sort()

# Split the dataset into train-validate splits 
train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size = 0.2, random_state = 1)

# Move the splits into their folders
move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val')
move_files_to_folder(train_labels, 'labels/train')
move_files_to_folder(val_labels, 'labels/val')

yaml_path = os.path.join(args.yolov5_directory, "data")
yaml_file = os.path.join(yaml_path, args.yaml_file_name)
write_yaml(yaml_file)