# TuSimple Velocity Estimation Challenge

![](https://raw.githubusercontent.com/TuSimple/tusimple-benchmark/master/doc/velocity_estimation/assets/examples/dis1.jpeg)



The goal of this challenge is to estimate the motion and position of vehicles relative to the camera. 

## Description
For each test sequence, predict the planar velocity and position of certain vehicles relative to the camera on a given specific frame. All the velocity and displacement in the up/down direction is ignored in this dataset. The output from your system should be a 2d vector representing the velocity vector, and a 2d coordinate in meters representing the closest point of the vehicle to the camera for each vehicle. The output should be formatted similarly with the given ground truth, whose format will be defined in the following section.
## Dataset Size
For velocity estimation, we provide 1074 training clips, each containing 40 frames of 20 fps video. Test set contains 269 clips. We also provide 5066 supplementary training images, labeled with vehicle bounding boxes. You can use the supplementary training data to assist you during your training process.

## Directory Structure:
`benchmark_velocity_train.zip`:
```
      |----readme.md                  # description
      |
      |----calibration.txt            #intrinsic parameters of the used camera
      |----clips/                     # 1074 video clips
      |------|----...
      |------|----some_clip/              # images and json labels for each clip
      |------|--------|
      |------|--------|----imgs/              # 40 frames of 20 fps video recorded, 2 seconds in total
      |------|--------|
      |------|--------|----annotation.json    # json annotation of designated vehicles.
      |------|----...
```
`benchmark_velocity_test.zip`:
```
      |----readme.md                  # description
      |
      |----calibration.txt            #intrinsic parameters of the used camera
      |----clips/                     # 269 video clips
      |------|----...
      |------|----some_clip/              # images and json labels for each clip
      |------|--------|
      |------|--------|----imgs/              # 40 frames of 20 fps video recorded, 2 seconds in total
      |------|--------|
      |------|--------|----annotation.json    # json annotation of designated vehicles.
```
`benchmark_velocity_supp.zip`:
```
      |----readme.md              # description
      |
      |----annotation.json      # bounding box annotations
      |----supp_img/               # 5066 images
```      

### Demo
The [demo code](https://github.com/TuSimple/tusimple-benchmark/blob/master/example/velocity_demo.ipynb) shows the data format of the velocity estimation dataset and the usage of the evaluation tool.      

## Label Data Format

`benchmark_velocity.zip`:
 - calibration.txt: a text file containing the intrinsic parameters of the camera used, structured in a 3*3 matrix and the camera height to the ground.

Each of the training clip can be found under a clip folder named after a integer.
The files in the folder are structured as follows:
 - imgs/:  subfolder contains 40 frames of images recorded at 20 fps, the end of the which, 040.jpg, is the frame that ground truth annotation on, and the frame that needs to estimate velocity on.
 - annotation.json: a json file, containing the ground truth velocity and position for designated vehicles.

And the ground truth json file is structured as follows:
```
{ 
   [vehicle]: an array of [vehicle], defining the velocity and position of each vehicle in the image.
}

vehicle:
{
  "bbox": a json structure with 4 fields 'top','left','bottom','right': The axis-aligned rectangle specifying the extent of the vehicle in the image.
  "velocity": a float pair [x,y]. Relative planar velocity of the vehicle in meters per second. x direction is the same with the camera optical axis and y direction is vertical to x and towards right.
  "position": a float pair [x,y]. Planar position of the nearest point on vehicle in meters. x direction is the same with the camera optical axis, and y direction is vertical to x and towards right.
}
```
`benchmark_velocity_test.zip`:
 - calibration.txt: a text file containing the intrinsic parameters of the camera used, structured in a 3*3 matrix and the camera height to the ground.

Each of the test clip can be found under a clip folder named after a integer.
The files in the folder are structured as follows:
 - imgs/:  subfolder contains 40 frames of images recorded at 20 fps, the end of the which, 040.jpg, is the frame that ground truth annotation on, and the frame that needs to estimate velocity on.
 - annotation.json: a json file, containing the bounding box for designated vehicles you need to estimate velocity and position on.

And the annotation json file is structured as follows:
```
{ 
   [bbox]: an array of [bbox], defining the position of each vehicle on the image.
}

bbox:
{
  "bbox": a json structure with 4 fields 'top','left','bottom','right': The axis-aligned rectangle specifying the extent of the vehicle in the image.
}
```
`benchmark_velocity_supp.zip`:
  - supp_img/: folder contains all the training images, named in 4 digit numbers.
  - annotation.json: a json file, containing the ground truth bounding box for all vehicles in all training images, structured as follows:
```
{
  [img]: an array of [img], representing the ground truth bounding box annotations for each image.
}

img:
{
  "file_name": a string representing the image file name.
  "bbox": a list of json structure [{'left', 'top', 'bottom', 'right'}], each representing the axis-aligned rectangle specifying the extend of a vehicle in this image.
}
```

## Result Submission
Your submission should contain a single json file, structured as follows:
```
{
   [frame]: an array of your result for each frame, sorted in the same way with the order of testing clips.
}

frame:
{
   [vehicle]: an array of your result for each designated vehicle in a certain frame, formatted in a same structre with the ground-truth data.
}

vehicle:
{
     "bbox": a json structure with 4 fields 'top','left','bottom','right': The axis-aligned rectangle specifying the given bounding box.
     "velocity": a float pair [x,y]. Predicted relative planar velocity of the vehicle in meters per second. x direction is the same with the camera optical axis and y direction is vertical to x and towards right.
     "position": a float pair [x,y]. Predicted planar position of the nearest point on vehicle in meters. x direction is the same with the camera optical axis, and y direction is vertical to x and towards right.
}
```
For our competition, you are required to provide a per-vehicle running time and the computing environment configuration for your method along with your submission. This information will not be included in the ranking.

## Evaluation Protocol
The metric we use in evaluating velocity estimation is Mean Squared Velocity Error:

<img src="https://latex.codecogs.com/gif.latex?$$E_v&space;=&space;\frac{\sum_{c\in&space;C}\|V^{gt}_c-V^{est}_c\|^2}{|C|}$$"/>

with <img src="https://latex.codecogs.com/gif.latex?$C$"/> denotes the set of submitted results for each vehicle, <img src="https://latex.codecogs.com/gif.latex?$V^{gt}_c$"/> represents the ground truth velocity for a certain vehicle, and <img src="https://latex.codecogs.com/gif.latex?$V^{est}_c$"/> represents the estimated velocity for that vehicle. Similarly, we use Mean Squared Position Error to evaluate position esitimation: 

<img src="https://latex.codecogs.com/gif.latex?$$E_p&space;=&space;\frac{\sum_{c\in&space;C}\|P^{gt}_c-P^{est}_c\|^2}{|C|}$$"/>

<img src="https://latex.codecogs.com/gif.latex?$P^{gt}_c$"/> represents the ground truth position of the nearest point on a certain vehicle, and <img src="https://latex.codecogs.com/gif.latex?$P^{est}_c$"/> represents the estimated position of the nearest point on such vehicle.

We classifiy test vehicles by its relative distance to the camera into three classes: Near(0-20m), Medium(20-45m), and Far(45m+). We evaluate the performance seperately on these three classes, and average them together to get the final evaluation score. For our competition, we rank your algorithm only based on the performance of velocity estimation.

