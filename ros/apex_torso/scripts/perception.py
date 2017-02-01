#!/usr/bin/env python
import rospy
from apex.perception import Perception

rospy.init_node('perception')
Perception().run()
rospy.spin()
