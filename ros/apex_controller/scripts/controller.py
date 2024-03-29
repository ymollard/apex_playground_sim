#!/usr/bin/env python
import rospy
import json
from os.path import join
from rospkg import RosPack
from apex.controller import Perception, Learning, Torso, Ergo
from trajectory_msgs.msg import JointTrajectory
from std_msgs.msg import UInt32


class Controller(object):
    def __init__(self):
        self.rospack = RosPack()
        with open(join(self.rospack.get_path('apex_playground'), 'config', 'general.json')) as f:
            self.params = json.load(f)
        self.torso = Torso()
        self.ergo = Ergo()
        self.learning = Learning()
        self.perception = Perception()
        self.iteration = -1  # -1 means "not up to date"
        rospy.Subscriber('/apex_playground/iteration', UInt32, self._cb_iteration)
        rospy.loginfo('Controller fully started!')

    def _cb_iteration(self, msg):
        self.iteration = msg.data

    def reset(self, slow=False):
        self.torso.reset(slow)

    def run(self):
        nb_iterations = rospy.get_param('/apex_playground/iterations')
        while not rospy.is_shutdown() and self.iteration < nb_iterations:
            if self.iteration % self.params['ergo_reset'] == 1:
                self.ergo.reset(True)
            if self.iteration != -1:
                rospy.logwarn("#### Iteration {}/{}".format(self.iteration + 1, nb_iterations))
                if self.perception.help_pressed():
                    rospy.sleep(1.5)  # Wait for the robot to fully stop
                    recording = self.perception.record(human_demo=True, nb_points=self.params['nb_points'])
                    self.reset(slow=True)
                else:
                    trajectory = self.learning.produce().torso_trajectory
                    self.torso.execute_trajectory(trajectory)  # TODO: blocking, non-blocking, action server?
                    recording = self.perception.record(human_demo=False, nb_points=self.params['nb_points'])
                    recording.demo.torso_demonstration = JointTrajectory()
                    self.reset()
                self.learning.perceive(recording.demo)  # TODO non-blocking
                # Many blocking calls: No sleep?


rospy.init_node("apex_playground_controller")
Controller().run()
