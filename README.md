# Human Motion Detection using Peeking Duck

## Purpose
The purpose of this is to detect the motion of humans for surveilance. Perhaps this will be useful for security ??

## Installation
Create a conda environment using `conda.yml` with the command below.
```
conda env create -f conda.yml
```

> Note: for users with ARM-based devices such as Raspberry Pi or Apple Silicon Mac, please refer to AISG Peeking Duck for [installation instructions.](https://peekingduck.readthedocs.io/en/stable/getting_started/03_custom_install.html)

## Input Data
Please ensure that there is input video in the `data` folder and change the *source* in `pipeline_config.yml` accordingly.

If you are using webcame live feed, please indicate '0' for *source* in `pipeline_config.yml`.

## Custom Node
A custom node was added to detect movement of tracking objects from `mode.jde` node.

The inputs for this node are: `img`, `bboxes` and `obj_attrs`. These are required to identify objects that are tracked.

The function of this node is to compare the previous and current position of bboxes of each tracking object and check if there is any changes. If there is a change, it means that the object has moved. This will change the color of bbox from `CHAMPAGNE` to `TOMATO`.

## Run
To run the pipeline, enter the following command in your peekingduck environment:
```
peekingduck run
```

## Output

__LEGEND__:<br>
CHAMPAGNE - stationary objects, <br>
TOMATO - moving objects <br>
Numbers are their tracking ID

![Result.gif](./images/people_walking.gif)

