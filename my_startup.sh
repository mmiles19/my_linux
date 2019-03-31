#!/bin/bash

export ROS_MASTER_URI=http://192.168.0.120:11311
source ~/compass_ws/devel/setup.bash
roslaunch ~/compass_ws/src/compass_node/launch/compass_node.launch
