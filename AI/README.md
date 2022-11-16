### Steps for AI Training
- Create `annotations` and `images` directories in the same directory as [setup.py](setup.py)
- Place images and annotations into the respective directories
- Run `python3 setup.py`
- Change working directory (cd) to the [yolov5 directory](yolov5)
- Run `python3 train.py --img 640 --cfg models/yolov5?.yaml --hyp data/hyp.scratch.yaml --batch-size 32 --epochs 100 --data data/data.yaml --workers 24 --project pokedex --name train1`
  - **img:** the training image resolution - recommended is 640 unless higher resolution (such as 1280) is needed for small objects
  - **cfg:** network architecture yaml file - four options for ? are **s**, **m**, **l**, **x** - the larger (more complex) the model, the greater the accuracy but lower the speed
  - **hyp:** hypeparameters file
  - **batch-size:** batch size - should use the highest batch size that hardware allows
  - **epochs:** number of training epochs
  - **data:** data file - created when running setup.py
  - **workers:** "the number of CPU cores used. If you are training DDP Multi-GPU then this is the number of CPU cores used per GPU" - not entirely sure what this means (maybe it's the number of threads?) so just keep it at 24 I guess
  - **project, name:** save weights to project/name
- Run `val.py --weights pokedex/train1/weights/best.pt --data hyp.scratch.yaml --task test --project pokedex --name test1`
  - **weights:** weights to test
  - **data:** data file - created when running setup.py
  - **project, name:** save test results

**Note:** Final weights stored in `pokedex/train1/weights/best.pt`
