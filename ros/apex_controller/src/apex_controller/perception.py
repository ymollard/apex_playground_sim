from std_msgs.msg import Bool, UInt8
from rospkg import RosPack
from os.path import join
from apex_msgs.srv import RecordRequest, Record
import rospy
import json


class Perception(object):
    def __init__(self):
        self.services = {'record': {'name': '/apex_playground/perception/record', 'type': Record}}
        for service_name, service in self.services.items():
            rospy.loginfo("Controller is waiting service {}...".format(service['name']))
            rospy.wait_for_service(service['name'])
            service['call'] = rospy.ServiceProxy(service['name'], service['type'])
        rospy.Subscriber('/apex_playground/ergo/button', Bool, self._cb_help_pressed)
        self.button_pressed = False
        self.last_press = rospy.Time(0)
        self.rospack = RosPack()
        with open(join(self.rospack.get_path('apex_playground'), 'config', 'perception.json')) as f:
            self.params = json.load(f)

    def _cb_help_pressed(self, msg):
        if msg.data and rospy.Time.now() - self.last_press > rospy.Duration(self.params['duration_between_presses']):
            rospy.logwarn("User demonstration requested, wait till the end of this iteration...")
            self.button_pressed = True
            self.last_press = rospy.Time.now()

    def help_pressed(self):
        pressed = self.button_pressed
        self.button_pressed = False
        return pressed

    def record(self, human_demo, nb_points):
        call = self.services['record']['call']
        return call(RecordRequest(human_demo=Bool(data=human_demo), nb_points=UInt8(data=nb_points)))