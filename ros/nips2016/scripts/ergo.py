#!/home/poppy/miniconda/bin/python
import rospy
from apex_playground.ergo import Ergo

rospy.init_node('ergo')
Ergo().run()
