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
    parser.add_argument("-a", "--annotations-directory", type=str, default="annotations")
    return parser.parse_args(args)

args = parse_opt(sys.argv[1:])
random.seed(20439472)

# Function to get the data from XML Annotation
def extract_classes_from_xml(xml_file):
    root = ET.parse(xml_file).getroot()
    
    # Parse the XML Tree
    for elem in root:
        if elem.tag == "object":
            for subelem in elem:
                if subelem.tag == "name":
                    if subelem.text not in classes:
                        classes.append(subelem.text)
                        print(subelem.text)

classes = []

annotations = [os.path.join(args.annotations_directory, x) for x in os.listdir(args.annotations_directory) if x[-3:] == "xml"]
annotations.sort()

for ann in tqdm(annotations):
    info_dict = extract_classes_from_xml(ann)