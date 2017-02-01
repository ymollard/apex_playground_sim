#!/usr/bin/env python
import rospy
from apex.torso import Torso

rospy.init_node('torso')
Torso().run()
