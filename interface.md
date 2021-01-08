
#连接接口：
本ros+gazebo仿真平台使用rosbridge_suit算法包生成websocket服务器

websocket服务器接口为  http://116.85.7.81:5901
请按照需求自行编写websocket客户端获取云端topic信息。

rosbridge_suit协议详见<https://github.com/RobotWebTools/rosbridge_suite/blob/groovy-devel/ROSBRIDGE_PROTOCOL.md>

示例：
unity与ros的通信详见<https://github.com/siemens/ros-sharp>
浏览器与ros的通信详见<https://github.com/RobotWebTools/roslibjs>

#gazebo发布的ros话题接口
##车的6dof位姿
1. ros topic名称：
/ground_truth/robot_state

2. ros_message文件：
/ground_truth/robot_state话题发布的gazebo_msgs/ModelState.msg数据结构：
string model_name           # model to set state (pose and twist)
geometry_msgs/Pose pose     # desired pose in reference frame
geometry_msgs/Twist twist   # desired twist in reference frame
string reference_frame      # set pose/twist relative to the frame of this entity (Body/Model)
                            # leave empty or "world" or "map" defaults to world-frame
##zed双目相机
1. ros topic名称(最主要的加粗显示)：
**/stereocamera/left/camera_info**
**/stereocamera/left/image_raw**
**/stereocamera/left/image_raw/compressed**
/stereocamera/left/image_raw/compressed/parameter_descriptions
/stereocamera/left/image_raw/compressed/parameter_updates
/stereocamera/left/image_raw/compressedDepth
/stereocamera/left/image_raw/compressedDepth/parameter_descriptions
/stereocamera/left/image_raw/compressedDepth/parameter_updates
/stereocamera/left/image_raw/theora
/stereocamera/left/image_raw/theora/parameter_descriptions
/stereocamera/left/image_raw/theora/parameter_updates
/stereocamera/left/parameter_descriptions
/stereocamera/left/parameter_updates
**/stereocamera/right/camera_info**
**/stereocamera/right/image_raw**
**/stereocamera/right/image_raw/compressed**
/stereocamera/right/image_raw/compressed/parameter_descriptions
/stereocamera/right/image_raw/compressed/parameter_updates
/stereocamera/right/image_raw/compressedDepth
/stereocamera/right/image_raw/compressedDepth/parameter_descriptions
/stereocamera/right/image_raw/compressedDepth/parameter_updates
/stereocamera/right/image_raw/theora
/stereocamera/right/image_raw/theora/parameter_descriptions
/stereocamera/right/image_raw/theora/parameter_updates
/stereocamera/right/parameter_descriptions
/stereocamera/right/parameter_updates
2. ros_message文件：
* .../camera_info话题发布的sensor_msgs/CameraInfo.msg数据结构：
   std_msgs/Header header
uint32 height
uint32 width
string distortion_model
float64[] D
float64[9] K
float64[9] R
float64[12] P
uint32 binning_x
uint32 binning_y
sensor_msgs/RegionOfInterest roi
* .../image_raw话题发布的sensor_msgs/Image数据结构：
std_msgs/Header header
uint32 height
uint32 width
string encoding
uint8 is_bigendian
uint32 step
uint8[] data
* .../image_raw/compressed话题发布的sensor_msgs/CompressedImage.msg数据结构：
std_msgs/Header header
string format
uint8[] data
##Kinect相机
1. ros topic名称(最主要的加粗显示)：
**/camera/depth/camera_info**//传输深度相机内参
**/camera/depth/image_raw**    //传输depth图
**/camera/rgb/camera_info**//传输rgb相机内参
**/camera/rgb/image_raw**   //传输rgb图
**/camera/rgb/image_raw/compressed**//传输压缩过的rgb图
/camera/rgb/image_raw/compressed/parameter_descriptions
/camera/rgb/image_raw/compressed/parameter_updates
/camera/rgb/image_raw/compressedDepth
/camera/rgb/image_raw/compressedDepth/parameter_descriptions
/camera/rgb/image_raw/compressedDepth/parameter_updates
/camera/rgb/image_raw/theora
/camera/rgb/image_raw/theora/parameter_descriptions
/camera/rgb/image_raw/theora/parameter_updates
2. ros_message文件见zed双目相机的介绍
##激光ladar
1. ros topic名称
/laser/scan
2. ros_message文件：
* /laser/scan话题发布的sensor_msgs/PointCloud2数据结构：
std_msgs/Header header
uint32 height
uint32 width
sensor_msgs/PointField[] fields
bool is_bigendian
uint32 point_step
uint32 row_step
uint8[] data
bool is_dense
##Imu
1. ros topic名称(最主要的加粗显示)
**/imu/data**
/imu/data/accel/parameter_descriptions
/imu/data/accel/parameter_updates
/imu/data/bias
/imu/data/rate/parameter_descriptions
/imu/data/rate/parameter_updates
/imu/data/yaw/parameter_descriptions
/imu/data/yaw/parameter_updates
2. ros_message文件：
* /imu/data话题发布的sensor_msgs/Imu.msg数据结构：
std_msgs/Header header
geometry_msgs/Quaternion orientation
float64[9] orientation_covariance
geometry_msgs/Vector3 angular_velocity
float64[9] angular_velocity_covariance
geometry_msgs/Vector3 linear_acceleration
float64[9] linear_acceleration_covariance

