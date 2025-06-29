#!/usr/bin/env python
# filepath: /home/mohab/thd-mss2/autonomous-container/second-attempt/ros-2023-thd/turtlebot3_ws/src/maze_navigator/scripts/rrt_initializer.py

import rospy
from geometry_msgs.msg import PointStamped
import time

def initialize_rrt():
    rospy.init_node('rrt_initializer', anonymous=True)
    pub = rospy.Publisher('/clicked_point', PointStamped, queue_size=10)
    
    # Get boundary points from parameters
    boundary = eval(rospy.get_param('~boundary', '[[2.92, 3.40], [2.85, -2.41], [-2.2, -1.7], [-2.2, 2.8]]'))
    init_point = eval(rospy.get_param('~init_point', '[0.0, 0.0]'))
    
    # Wait for connections
    time.sleep(5)
    
    # Create PointStamped message
    point = PointStamped()
    point.header.frame_id = "map"
    point.header.stamp = rospy.Time.now()
    
    # Publish boundary points
    for b in boundary:
        point.point.x = b[0]
        point.point.y = b[1]
        point.point.z = 0.0
        pub.publish(point)
        rospy.loginfo("Published boundary point: [%f, %f]", b[0], b[1])
        time.sleep(0.5)
    
    # Publish initialization point
    point.point.x = init_point[0]
    point.point.y = init_point[1]
    point.point.z = 0.0
    pub.publish(point)
    rospy.loginfo("Published initialization point: [%f, %f]", init_point[0], init_point[1])

if __name__ == '__main__':
    try:
        initialize_rrt()
    except rospy.ROSInterruptException:
        pass
