#!/usr/bin/env bash

# Activate SWAP first!
if [ ! -e /dev/sda1  ]; then
    echo -e "Please insert USB key to /dev/sda1 for swap before continuing"
    exit 1
fi
sudo swapon /dev/sda1

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python python-dev cmake
sudo apt-get install -y htop uptimed git

sed -i.bak -e "s/#alias /alias /g" /home/pi/.bashrc

# Python packages
wget bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install jupyter-notebook

# ROS Kinectic
mkdir -p /home/pi/ros_ws/src
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu jessie main" > /etc/apt/sources.list.d/ros-latest.list'
wget https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -O - | sudo apt-key add -
sudo apt-get install -y python-rosdep python-rosinstall-generator python-wstool python-rosinstall build-essential cmake
sudo apt-get install -y python-setuptools python-yaml python-distribute python-docutils python-dateutil python-six
sudo pip install rosdep rosinstall_generator wstool rosinstall empy
cd /home/pi/ros_ws
sudo rosdep init
rosdep update
rosinstall_generator ros_comm --rosdistro kinetic --deps --wet-only --tar > kinetic-roscomm-wet.rosinstall
wstool init src kinetic-roscomm-wet.rosinstall

# Fix assimp as in the tuto
mkdir -p /home/pi/ros_ws/external_src
cd /home/pi/ros_ws/external_src
wget http://sourceforge.net/projects/assimp/files/assimp-3.1/assimp-3.1.1_no_test_models.zip/download -O assimp-3.1.1_no_test_models.zip
unzip assimp-3.1.1_no_test_models.zip
cd assimp-3.1.1
cmake .
make -j4
sudo make install

# Recover ROS install
cd /home/pi/ros_ws/
rosdep install -y --from-paths src --ignore-src --rosdistro kinetic -r --os=debian:jessie
sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/kinetic -DCMAKE_MODULE_PATH=/usr/share/cmake-3.0/Modules

if [ $? -eq 0 ]; then
    echo -e "\nexport LC_ALL=C # Fix: terminate called after throwing an instance of 'std::runtime_error' what():  locale::facet::_S_create_c_locale name not valid\n" >> /home/pi/.bashrc
    echo -e "if [ -f /home/pi/ros_ws/devel_isolated/setup.bash ]; then\n source /home/pi/ros_ws/devel_isolated/setup.bash\nfi\n " >> /home/pi/.bashrc
else
    echo -e "\e[31mROS comm install failed, exiting\e[0m"
    exit 1
fi

# Poppy Torso/Ergo (~2hrs to install and compile)
sudo apt-get install -y liblapack-dev gfortran        # Required by scipy
sudo pip install poppy-ergo-jr poppy-torso

# APEX playground files
mkdir -p /home/pi/Repos
cd /home/pi/Repos
git clone https://github.com/ymollard/apex_playground.git
ln -s apex_playground/ros/ /home/pi/ros_ws/src/apex_playground

cd /home/pi/ros_ws
sudo ./src/catkin/bin/catkin_make_isolated -DCMAKE_MODULE_PATH=/usr/share/cmake-3.0/Modules

# In case of fail with Eigen3 add -DCMAKE_MODULE_PATH=/usr/share/cmake-3.0/Module or
# Replace find_package(Eigen3) by
# ```
#    find_package( PkgConfig )
#    pkg_check_modules( EIGEN3 REQUIRED eigen3 )
#    include_directories( ${EIGEN3_INCLUDE_DIRS} )
# ```
# in ros_ws/src/eigen_stl_containers/CMakeLists.txt
# in ros_ws/src/geometric_shapes/CMakeLists.txt

# Done, leaving...
if [ $? -eq 0 ]; then
    sudo swapoff /dev/sda1
fi
