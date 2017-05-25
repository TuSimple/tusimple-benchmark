# Guideline for Velocity Estimation Challenge

## Download
The data of lane detection challenge is available for download here.

[velocity_estimation [246 training image sequences]](https://s3-us-west-2.amazonaws.com/benchmark.tusimple.ai/benchmark_velocity.zip)
[supplementary_data [919 training images]](https://s3-us-west-2.amazonaws.com/benchmark.tusimple.ai/benchmark_velocity_supp.zip)

## Annotation Format

Each of the training clip can be found under a clip folder named in 3 digit numbers.
The files in the folder are structured as follows:
 - img/:  subfolder contains 60 frames of images recorded at 30 fps, the end of the which, 060.jpg, is the frame that ground truth annotation on, and the frame that needs to estimate velocity on.
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

`benchmark_velocity_supp.zip`:
  - supp_img/: folder contains all the training images, named in 4 digit numbers.
  - annotation.json: a json file, containing the ground truth bounding box for all vehicles in all training images, structured as follows:
```
{
[img]: an array of [img], representing the ground truth bounding box annotation for each image.
}

img:
{
"file_name": a string representing the image file name.
"bbox": a list of json structure [{'left', 'top', 'bottom', 'right'}], each representing the axis-aligned rectangle specifying the extend of a vehicle in this image.
}
```

## Testing Indication format
The testing data contains only "bbox" field of the ground truth format, indicating the vehicle whose velocity needs to be estimated. structured as follows:
```
{[ "bbox": {'top', 'left', 'bottom', 'right'}]}
```

## Results format

The results format closely mimics the format of the gound truth as described on the previous section. A seperate result json file should be created for each seperate clip, named after such clip, containing the exact bouding box provided in the testing indication file, and velocity and position your algorithm estimated.
```
{[  "bbox": {'top', 'left', 'bottom', 'right'}
   "velocity": [x,y]
   "position": [x,y]
 ]}
```

## Evaluation
The evaluation code, as described in [here](http://benchmark.tusimple.ai/#/challenge/velocity/readme), can be found in [demo code](https://github.com/TuSimple/tusimple-benchmark/blob/master/example/velocity_demo.ipynb)
