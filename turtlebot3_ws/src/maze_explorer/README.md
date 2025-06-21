# Maze Explorer Package

## Overview

The `maze_explorer` package is a ROS (Robot Operating System) package designed for autonomous maze exploration using a TurtleBot3 Burger robot. It combines SLAM (Simultaneous Localization and Mapping), basic navigation, and simple exploration algorithms to enable a robot to autonomously navigate and map unknown maze environments.

## Package Structure

```
maze_explorer/
├── CMakeLists.txt          # Build configuration
├── package.xml             # Package dependencies and metadata
├── scripts/
│   └── maze_explorer_node.py  # Main exploration node
├── launch/
│   └── maze_exploration.launch  # Complete system launch file
├── worlds/
│   └── maze_3_6x6.world    # Gazebo maze world file
└── models/                 # Gazebo model files (if any)
```

## Features

- **Autonomous Maze Exploration**: Robot explores unknown maze environments
- **SLAM Integration**: Uses gmapping for simultaneous localization and mapping
- **Simple Wall-Following**: Basic exploration algorithm based on laser scan data
- **Gazebo Simulation**: Complete simulation environment with maze world
- **TurtleBot3 Integration**: Designed specifically for TurtleBot3 Burger robot

## Dependencies

This package requires the following ROS packages:
- `rospy` - Python ROS client library
- `std_msgs` - Standard ROS message types
- `geometry_msgs` - Geometry-related message types
- `nav_msgs` - Navigation message types
- `sensor_msgs` - Sensor message types
- `tf2_ros` - Transform library
- `gmapping` - SLAM algorithm
- `turtlebot3_description` - TurtleBot3 robot description
- `turtlebot3_bringup` - TurtleBot3 startup scripts
- `gazebo_ros` - Gazebo simulation interface

## How It Works

### 1. Simulation Environment
The package launches a Gazebo simulation environment with:
- A predefined 6x6 maze world
- Physics simulation
- TurtleBot3 Burger robot model spawned at position (0.5, 0.5)

### 2. Robot Components
- **Robot State Publisher**: Publishes robot's joint states and transforms
- **Joint State Publisher**: Handles robot joint information
- **Laser Scanner**: Provides 360-degree distance measurements for obstacle detection

### 3. SLAM (Simultaneous Localization and Mapping)
Uses the `gmapping` algorithm to:
- Build a map of the environment as the robot explores
- Localize the robot within the map
- Publish map data on the `/map` topic
- Maintain coordinate frame transformations (map ↔ odom ↔ base_footprint)

### 4. Exploration Algorithm
The `maze_explorer_node.py` implements a simple wall-following exploration strategy:

```python
# Simplified exploration logic
if min_front_distance > 0.5:
    # Path is clear - move forward
    robot.move_forward(speed=0.2)
else:
    # Obstacle detected - turn
    robot.turn(angular_speed=0.5)
```

### 5. Data Flow
1. **Laser Scanner** → Publishes distance data to `/scan`
2. **Gmapping** → Processes laser + odometry → Publishes map to `/map`
3. **Explorer Node** → Reads `/scan` and `/map` → Publishes movement commands to `/cmd_vel`
4. **Robot** → Executes movement commands → Updates odometry

## Usage

### Prerequisites
Ensure you have the required packages installed:
```bash
sudo apt install ros-noetic-gmapping
sudo apt install ros-noetic-turtlebot3-simulations
sudo apt install ros-noetic-turtlebot3-slam
```

### Running the System

1. **Build the package**:
```bash
cd /ros_ws/turtlebot3_ws
catkin_make
source devel/setup.bash
```

2. **Set TurtleBot3 model** (add to ~/.bashrc for persistence):
```bash
export TURTLEBOT3_MODEL=burger
```

3. **Launch the complete system**:
```bash
roslaunch maze_explorer maze_exploration.launch
```

This single command will:
- Start Gazebo with the maze world
- Spawn the TurtleBot3 robot
- Initialize SLAM (gmapping)
- Start the exploration node

### Monitoring the System

You can monitor the system using various ROS tools:

```bash
# View active topics
rostopic list

# Monitor laser scan data
rostopic echo /scan

# Monitor map data
rostopic echo /map

# Monitor robot movement commands
rostopic echo /cmd_vel

# View the map in RViz
rviz
```

## Key Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/scan` | `sensor_msgs/LaserScan` | Laser scanner distance measurements |
| `/map` | `nav_msgs/OccupancyGrid` | SLAM-generated map |
| `/odom` | `nav_msgs/Odometry` | Robot odometry information |
| `/cmd_vel` | `geometry_msgs/Twist` | Robot movement commands |

## Configuration Parameters

The gmapping SLAM algorithm can be tuned through various parameters:
- `map_update_interval`: How often to update the map (2.0 seconds)
- `maxUrange`: Maximum laser range to use (3.0 meters)
- `particles`: Number of particles for localization (30)
- `linearUpdate`: Distance robot must move before updating (1.0 meter)
- `angularUpdate`: Angle robot must turn before updating (0.5 radians)

## Limitations

- **Simple Exploration**: Uses basic wall-following, not optimal path planning
- **No Goal Planning**: Doesn't set specific exploration goals or frontiers
- **Single Robot**: Designed for single robot exploration only
- **Static Environment**: Assumes the maze doesn't change during exploration

## Future Enhancements

Potential improvements for this package:
1. **Advanced RRT Exploration**: Integration with `rrt_exploration` package
2. **Frontier-Based Exploration**: More intelligent exploration strategy
3. **Path Planning**: Integration with `move_base` for navigation
4. **Multi-Robot Support**: Coordinate multiple robots
5. **Dynamic Obstacle Handling**: Handle moving obstacles
6. **Exploration Metrics**: Track exploration progress and efficiency

## Troubleshooting

### Common Issues

1. **"gmapping not found"**: Install gmapping package
```bash
sudo apt install ros-noetic-gmapping
```

2. **"Multiple robot_state_publisher nodes"**: This launch file ensures only one instance runs

3. **"Transform errors"**: Wait for SLAM to initialize properly (takes ~10-15 seconds)

4. **Robot not moving**: Check that `/cmd_vel` topic is being published and robot is receiving commands

### Debug Commands

```bash
# Check if all nodes are running
rosnode list

# Check transform tree
rosrun tf view_frames

# Monitor system status
rostopic hz /scan
rostopic hz /map
rostopic hz /cmd_vel
```

## License

This package is provided under the MIT License (or specify your preferred license).

## Author

[Your Name/Organization]

---

*This package demonstrates basic principles of autonomous robot exploration and can serve as a foundation for more advanced maze-solving and exploration