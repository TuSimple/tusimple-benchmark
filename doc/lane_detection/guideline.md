# Guideline for Lane Detection Challenge

## Download
The full introduction is on the [page](https://tusimple.github.io/tusimple-benchmark/#/challenge/lane/readme). 

The data of lane detection challenge is available for download here.

[lane_detection [9 GB, 2858 labelled frame]](https://s3-us-west-2.amazonaws.com/benchmark.tusimple.ai/lane_data.zip)

## Data Format
For one frame, the format of ground-truth and prediction is following.
```
{
'raw_file': str. Clip file path.
'lanes': list. A list of four lanes - [inner_left_lane, inner_right_lane, outer_left_lane, outer_right_lane].
	for each list of one lane, the elements are width values on image.
'h_samples': list. A list of height values corresponding to the 'lanes', which means len(h_samples) == len(lanes[i])
}
```
You can `zip`  each lane in `lanes` with `h_samples`to get sequential points of one lane.

The demo code (see below) will show how to do this. We assume that for one lane boundary there is no situation where multiple points are on one `h_sample`.

## Evaluation
The evaluation process is described in the [page](https://tusimple.github.io/tusimple-benchmark/#/challenge/lane/readme).

In the demo code we present how to evaluate one frame's prediction.

## Demo
The [demo code](https://github.com/TuSimple/tusimple-benchmark/blob/master/example/lane_demo.ipynb) shows how to evaluate one frame.

