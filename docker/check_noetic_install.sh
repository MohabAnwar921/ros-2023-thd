#!/bin/bash
echo "=== ROS Installation Check ==="
echo "ROS directories:"
ls -la /opt/ros/ 2>/dev/null || echo "No /opt/ros/ directory"

echo -e "\nInstalled ROS Noetic packages:"
dpkg -l | grep ros-noetic | wc -l
echo "packages found"

echo -e "\nMain ROS distributions installed:"
dpkg -l | grep -E "ros-noetic-(desktop-full|desktop|ros-base|ros-core)"

echo -e "\nROS environment variables:"
echo "ROS_DISTRO: ${ROS_DISTRO:-not set}"
echo "ROS_ROOT: ${ROS_ROOT:-not set}"