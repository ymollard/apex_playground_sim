import rospy
from numpy import array
from apex_msgs.srv import SetIteration, SetIterationRequest, SetFocus, SetFocusRequest, Assess, AssessRequest
from apex_msgs.msg import Interests
from std_msgs.msg import String, Bool, UInt32


class UserServices(object):
    def __init__(self):
        self.services = {'set_iteration': {'name': '/apex_playground/learning/set_iteration', 'type': SetIteration},
                         'set_focus': {'name': '/apex_playground/learning/set_interest', 'type': SetFocus},
                         'assess': {'name': '/apex_playground/learning/assess', 'type': Assess}}

        rospy.Subscriber('/apex_playground/learning/interests', Interests, self._cb_interests)
        rospy.Subscriber('/apex_playground/learning/current_focus', String, self._cb_focus)
        rospy.Subscriber('/apex_playground/learning/user_focus', String, self._cb_user_focus)
        rospy.Subscriber('/apex_playground/learning/ready_for_interaction', Bool, self._cb_ready)

        self.interests = {}
        self.current_focus = ""
        self.user_focus = ""
        self.ready_for_interaction = False

        for service_name, service in self.services.items():
            rospy.loginfo("User node is waiting service {}...".format(service['name']))
            rospy.wait_for_service(service['name'])
            service['call'] = rospy.ServiceProxy(service['name'], service['type'])

        rospy.loginfo("User node started!")

    def _cb_interests(self, msg):
        self.interests = dict(zip(msg.names, array(map(lambda x: x.data, msg.interests)).reshape(msg.num_iterations.data, len(msg.names)).T.tolist()))

    def _cb_focus(self, msg):
        self.current_focus = msg.data

    def _cb_user_focus(self, msg):
        self.user_focus = msg.data

    def _cb_ready(self, msg):
        self.ready_for_interaction = msg.data

    def set_focus(self, space):
        call = self.services['set_focus']['call']
        return call(SetFocusRequest(space=space))

    def assess(self, assessment):
        call = self.services['assess']['call']
        return call(AssessRequest(goal=assessment))

    def set_iteration(self, iteration):
        call = self.services['set_iteration']['call']
        return call(SetIterationRequest(iteration=UInt32(data=int(iteration))))