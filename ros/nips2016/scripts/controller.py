#!/usr/bin/env python
import rospy
import json
from os.path import join
from rospkg import RosPack
from nips2016.controller import Perception, Learning, Torso, Ergo
from trajectory_msgs.msg import JointTrajectory
from std_msgs.msg import UInt32


class Controller(object):
    def __init__(self):
        self.rospack = RosPack()
        with open(join(self.rospack.get_path('nips2016'), 'config', 'general.json')) as f:
            self.params = json.load(f)
        self.torso = Torso()
        self.ergo = Ergo()
        self.learning = Learning()
        self.perception = Perception()
        self.iteration = 0
        rospy.Subscriber('/nips2016/iteration', UInt32, self._cb_iteration)
        rospy.loginfo('Controller fully started!')

    def _cb_iteration(self, msg):
        self.iteration = msg.data

    def reset(self):
        self.torso.reset()

    def run(self):
        nb_iterations = rospy.get_param('/nips2016/iterations')
        while not rospy.is_shutdown() and self.iteration < nb_iterations:
            rospy.loginfo("#### Iteration {}/{}".format(self.iteration + 1, nb_iterations))
            self.reset()
            if self.perception.help_pressed():
                rospy.sleep(1.5)  # Wait for the robot to fully stop
                recording = self.perception.record(human_demo=True, nb_points=self.params['nb_points'])
                self.learning.perceive(recording.torso_demonstration, recording.sensorial_demonstration)
            else:
                trajectory = self.learning.produce().torso_trajectory
                self.torso.execute_trajectory(trajectory)  # TODO: blocking, non-blocking, action server?
                recording = self.perception.record(human_demo=False, nb_points=self.params['nb_points'])
                self.learning.perceive(JointTrajectory(), recording.sensorial_demonstration)  # TODO non-blocking
            # Many blocking calls: No sleep?

rospy.init_node("nips2016_controller")
Controller().run()
