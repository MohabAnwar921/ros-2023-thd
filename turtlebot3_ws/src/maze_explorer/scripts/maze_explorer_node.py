#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid

class MazeExplorer:
    def __init__(self):
        rospy.init_node('maze_explorer_node', anonymous=True)
        
        # Publishers
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Subscribers
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        self.map_sub = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        
        self.laser_data = None
        self.map_data = None
        
        rospy.loginfo("Maze Explorer Node initialized")
        
    def laser_callback(self, msg):
        self.laser_data = msg
        
    def map_callback(self, msg):
        self.map_data = msg
        
    def explore(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if self.laser_data:
                # Simple wall following
                twist = Twist()
                ranges = self.laser_data.ranges
                min_front = min(ranges[0:30] + ranges[-30:])  # Front 60 degrees
                
                if min_front > 0.5:
                    twist.linear.x = 0.2
                    twist.angular.z = 0.0
                else:
                    twist.linear.x = 0.0
                    twist.angular.z = 0.5
                    
                self.cmd_vel_pub.publish(twist)
            rate.sleep()

if __name__ == '__main__':
    try:
        explorer = MazeExplorer()
        explorer.explore()
    except rospy.ROSInterruptException:
        pass