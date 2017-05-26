# Guideline for Lane Detection Challenge

## Download
The full introduction is on the [page](http://benchmark.tusimple.ai/#/challenge/lane/readme).

The data of the lane detection challenge is available for download here.

[lane_detection [9 GB, 2858 labelled frame]](https://s3-us-west-2.amazonaws.com/benchmark.tusimple.ai/lane_detection.zip)

## Data Format
For one frame, the format of ground-truth and prediction are as the following.
```
{
'raw_file': str. Clip file path.
'lanes': list. A list of four lanes. For each list of one lane, the elements are width values on image.
'h_samples': list. A list of height values corresponding to the 'lanes', which means len(h_samples) == len(lanes[i])
}
```
You can `zip`  each lane in `lanes` with `h_samples`to get sequential points of one lane.

The demo code (see below) will show how to do this.
We assume that for one lane, at the same `h_sample` there will be only one road mark point. In other words, we assume
the lane will not turn around.


## Evaluation
The evaluation process is described in the [page](http://benchmark.tusimple.ai/#/challenge/lane/readme).

In the demo code we present how to evaluate one frame's prediction.

## Demo
The [demo code](https://github.com/TuSimple/tusimple-benchmark/blob/master/example/lane_demo.ipynb) shows the data
format of the lane dataset and the usage of the evaluation tool.
