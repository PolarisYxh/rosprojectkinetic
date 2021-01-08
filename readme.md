# my ros Jackal's  package
sudo apt install ros--control* ros--gazebo-ros*
before roslaunch iqr_4b_bringup iqr_bringup.launch,have to open all the devices such as kinova
roslaunch iqr_4b_moveit_config iqr_4b_moveit_execute.launch//manipulate kinova arm
rosrun kinova_demo fingers_action_client.py j2n6s300 percent -- 100 100 100   //动指头的，最后三个数<0,100>之间
roslaunch iqr_4b_navigation gmapping_demo.launch//open navigation algorithm

## only jackal model
sudo apt-get install ros-kinetic-jackal-simulator ros-kinetic-jackal-desktop ros-kinetic-jackal-navigation//下载jackal所有包
roslaunch jackal_gazebo jackal_world1.launch//打开gazebo的jackal机器人
roslaunch iqr_4b_bringup zhikete_mars.launch//打开智科特机器人和mars_plane的gazebo
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch//键盘控制机器人，需要turtlebot3的包
roslaunch jackal_viz view_robot.launch//rviz控制机器人
rosrun save_rgbd_from_kinect2 save_rgbd_from_kinect2//保存rgbd图
roslaunch iqr_4b_bringup zhikete_academy.launch  //打开智科特机器人和图书馆场景
## document
iqr_4b_robot-master/iqr_4b_description/urdf/iqr_4b_robot.urdf.xacro   //整体智科特组装机器人的文件

## 自己写的python通过socket传输从ros节点获取的rgbd图片
save_rgbd_from_kinect2里面的 trans_rgbd_from_kinect.py是服务器，获取ros rgbd传输到客户端
rosrun save_rgbd_from_kinect2 trans_rgbd_from_kinect.py
save_rgbd_from_kinect2里面的get_rgbd.py是客户端，获取rgbd并保存

## ros+unity
roslaunch iqr_4b_bringup zhikete_mars.launch//打开智科特机器人和mars_plane的gazebo
rosrun iqr_4b_bringup joy_to_twist.py  //打开unity控制机器人的节点
ros_unity_pro/Assets/RosSharp/Scenes/ZhiketeScene.unity    //打开对应的火星 unity场景，在unity场景运行以后，可以方向键控制机器人运动
ros_unity_pro/Assets/RosSharp/Scenes/3D SCENE/AVP_Interior_Vol.2.unity     //打开房间场景

## 502
roslaunch iqr_4b_bringup zhikete_mars.launch  //打开月面仿真环境+zhikete机器车(该车目前含有./interface.pdf中所述各个传感器的接口)
### 加机械臂的小车
roslaunch iqr_4b_bringup zhikete_unity.launch  //打开室内仿真环境+zhikete机器车+受控制的机械臂(该车目前含有./interface.pdf中所述各个传感器的接口)
roslaunch j2n6s300_moveit_config j2n6s300_zhikete_gazebo_demo.launch
roslaunch iqr_4b_bringup 502_mars.launch    //打开月面仿真环境+502机器车(该车目前含有kinect,laser传感器，后续可以添加)
roslaunch a502_teleop turtlebot3_teleop.launch //打开键盘控制机器车运动程序，wasd控制运动
roslaunch a502_teleop ps3_teleop.launch //打开手柄，控制机器车运动程序，4、5轴控制运动，sudo jstest /dev/input/js0测试手柄接口，
```
sudo apt-get install ros-melodic-joy
sudo apt-get install ros-melodic-joystick-drivers
```

## 单独的机械臂
### 第1步
- roslaunch kinova_gazebo robot_launch.launch kinova_robotType:=j2n6s300 use_trajectory_controller:=true //打开gazebo的kinova，false可以用rqt控制角度
- rosrun kinova_control move_robot.py j2n6s300 //use_trajectory_controller:=true时，此命令控制机械臂复位
### 第2步
roslaunch j2n6s300_moveit_config j2n6s300_gazebo_demo.launch  //use_trajectory_controller:=true时,开启group用来控制机械臂运动
### 第3步
- rosrun kinova_arm_moveit_demo pick_place  //rviz中控制gazebo运动
- rviz:roslaunch   j2n6s300_moveit_config   j2n6s300_virtual_robot_demo.launch  //控制kinova rviz中机械臂运动，不控制gazebo
- roslaunch kinova_arm_moveit_demo phantomPoseTarget.launch   //用geomagic touch控制机械臂运动
rosdep 问题：sudo gedit /etc/hosts  #在文件末尾添加  151.101.84.133  raw.githubusercontent.com
sudo apt-get install ros-kinetic-moveit*
sudo apt-get install ros-kinetic-trac-ikmoveit


## 文件说明
a502_teleop里面是键盘控制机器车运动的脚本
asm_car_asm里面是502研究所8轮车的模型描述
iqr_4b_robot-master/iqr_4b_bringup里面是各个仿真环境的launch文件，是仿真环境入口，还有zhikete小车模型，月面及其他世界模型。
iqr_4b_robot-master/iqr_4b_moveit_config里面是机械臂相关launch文件，目前没用
iqr_4b_robot-master/iqr_4b_navigation里面是导航相关launch文件，运行导航包入口
iqr_pan_tilt-master里面是控制kinect相机云台的控制程序
kinova-ros-master里面是运行控制机械臂的包，目前没用
save_rgbd_from_kinect2里面是自己写的保存一些传感器信息的程序
