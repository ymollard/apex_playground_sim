import rospy
from apex_playground.srv import *


class Torso(object):
    def __init__(self):
        self.services = {'exec_torso': {'name': '/apex_playground/torso/execute', 'type': ExecuteTorsoTrajectory},
                         'reset_torso': {'name': '/apex_playground/torso/reset', 'type': Reset}}
        for service_name, service in self.services.items():
            rospy.loginfo("Controller is waiting service {}...".format(service['name']))
            rospy.wait_for_service(service['name'])
            service['call'] = rospy.ServiceProxy(service['name'], service['type'])

    def reset(self, slow):
        call = self.services['reset_torso']['call']
        return call(ResetRequest(slow=slow))

    def execute_trajectory(self, trajectory):
        call = self.services['exec_torso']['call']
        return call(ExecuteTorsoTrajectoryRequest(torso_trajectory=trajectory))

