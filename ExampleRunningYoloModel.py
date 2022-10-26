
# YOLOv5 PyTorch HUB Inference (DetectionModels only)
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # yolov5n - yolov5x6 or custom
image = 'https://ultralytics.com/images/zidane.jpg'  # file, Path, PIL.Image, OpenCV, nparray, list
results = model(image)  # inference

#Obtain results with .print(), .show(), .save(), .crop(), .pandas(), etc.
results.print()
results.show()  
