#!/home/poppy/miniconda/bin/python
import rospy
from apex.ergo import Ergo

rospy.init_node('ergo')
Ergo().run()
