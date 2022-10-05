from pathlib import Path

Path("images/train").mkdir(parents=True, exist_ok=True)
Path("images/val").mkdir(parents=True, exist_ok=True)
Path("images/test").mkdir(parents=True, exist_ok=True)

Path("annotations/train").mkdir(parents=True, exist_ok=True)
Path("annotations/val").mkdir(parents=True, exist_ok=True)
Path("annotations/test").mkdir(parents=True, exist_ok=True)

print("Place images in the images directory and annotations in the annotations directory.")