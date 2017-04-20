```
pip install --user -U rosdep rosinstall_generator wstool rosinstall
pip install empy
mkdir ros_ws
#alias cmake=/cm/shared/contrib/apps/cmake/bin/cmake
#mkdir install
#mkdir devel
#nano ros_ws/src/catkin/python/catkin/builder.py
## Search _cmd and repalce 'catkin' with the path hereabove
module add cmake/2.8.12.2
cmake --version   # > 2.8

cd
cd ros_ws
mkdir external && cd external
git clone https://github.com/ros/console_bridge.git
cd console_bridge
cmake .
make
CBRIDGE=`pwd`

cd ~/ros_ws
./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release -j12 -Dconsole_bridge_DIR=$CBRIDGE
