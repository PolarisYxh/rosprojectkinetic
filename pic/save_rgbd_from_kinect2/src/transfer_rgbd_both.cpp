/**
 *
 * 函数功能：采集iaikinect2输出的彩色图和深度图数据，并以文件的形式进行存储
 *
 *
 * 分隔符为　逗号'，'　　
 * 时间戳单位为秒(s)　精确到小数点后６位(us)
 *
 * maker:crp
 * 2017-5-13
 */

#include<iostream>
#include<string>
#include <stdlib.h>
#include <stdio.h>
#include <sstream>
#include <vector>

#include <ros/ros.h>
#include <ros/spinner.h>
#include <sensor_msgs/CameraInfo.h>
#include <sensor_msgs/Image.h>

#include "color_depth_msg/colordepth.h"

#include <std_msgs/String.h>

#include <cv_bridge/cv_bridge.h>//将ROS下的sensor_msgs/Image消息类型转化成cv::Mat。
#include<sensor_msgs/image_encodings.h>//头文件sensor_msgs/Image是ROS下的图像的类型，这个头文件中包含对图像进行编码的函数

#include <image_transport/image_transport.h>
#include <image_transport/subscriber_filter.h>
#include <opencv2/imgproc/imgproc.hpp>
#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include<iostream>
#include <fstream>
#include <sstream>

#include <X11/Xlib.h>
using namespace std;
using namespace cv;

Mat rgb, depth,depth1;
char successed_flag1 =0,successed_flag2=0;

string topic1_name = "/camera/rgb/image_raw"; //topic 名称
string topic2_name = "/camera/depth/image_raw";


//bool display_IMU5211( unsigned char buf[21] ,timeval time_stamp,string &out_result);
//void dispDepth(const cv::Mat &in, cv::Mat &out, const float maxValue);
void  callback_function_color( const sensor_msgs::Image::ConstPtr  image_data);
void  callback_function_depth( const sensor_msgs::Image::ConstPtr  image_data);
int main(int argc,char** argv)
{
    string out_result;
    color_depth_msg::colordepth cd;
    sensor_msgs::ImagePtr d_msg;
    sensor_msgs::ImagePtr c_msg;
    //namedWindow("image color",CV_WINDOW_AUTOSIZE);
    //namedWindow("image depth",CV_WINDOW_AUTOSIZE);
    ros::init(argc,argv,"kinect2_listen");
    if(!ros::ok())
             return 0;
    ros::NodeHandle n;
    ros::Subscriber sub1 = n.subscribe(topic1_name,50,callback_function_color);
    ros::Subscriber sub2 = n.subscribe(topic2_name,50,callback_function_depth);

    ros::Publisher picpub = n.advertise<color_depth_msg::colordepth>("color_depth_ref", 1000);
    ros::AsyncSpinner spinner(3); // Use 3 threads
    spinner.start();
   // string rgb_str, dep_str;

    while(ros::ok())
    {
        if( successed_flag1&&successed_flag2)
        {
                //gettimeofday(&time_val,&tz);//us
            //  time_stamp =time_val.tv_sec+ time_val.tv_usec/1000000.0;
            // ostringstream os_rgb;
                //os_rgb<<time_val.tv_sec<<"."<<time_val.tv_usec;
            // double k=0.000001*num1;
                //rgb_str = save_imagedata+"rgb/"+os_rgb.str()+".png";
            //rgb_str = save_imagedata+"rgb/"+std::to_string(k)+".png";
            //dep_str =save_imagedata+"depth/"+std::to_string(k)+".png";// 输出图像目录
            //imwrite(rgb_str,rgb);
            //imwrite(dep_str,depth);
                //fout_rgb<<os_rgb.str()<<",rgb/"<<os_rgb.str()<<".png\n";
            successed_flag1 = 0;
            successed_flag2 = 0;
            c_msg = cv_bridge::CvImage(std_msgs::Header(),"rgb8",rgb).toImageMsg();
            d_msg = cv_bridge::CvImage(std_msgs::Header(),"mono16",depth).toImageMsg();
            cd.depth = *d_msg;
            cd.color = *c_msg;
            picpub.publish(cd);
            //num1++;
            ros::spinOnce();
        }
    }

    ros::waitForShutdown();
    ros::shutdown();

    return 0;
}
void  callback_function_color(const sensor_msgs::Image::ConstPtr  image_data)
{
   cv_bridge::CvImageConstPtr pCvImage;// 声明一个CvImage指针的实例
    //   cout<<"the frame_id:"<<image_data->frame_id.c_str()<<endl;
//    cout<<"the image heigh"<<image_data->height<<endl;
//    cout<<"the image width"<<image_data->width<<endl;
//    cout<<"the image step"<<image_data->step<<endl;
//    cout<<"listen ...."<<endl;

   pCvImage = cv_bridge::toCvShare(image_data, image_data->encoding);//将ROS消息中的图象信息提取，生成新cv类型的图象，复制给CvImage指针
   pCvImage->image.copyTo(rgb);
    successed_flag1 = 1;
  // cv::waitKey(0);
}
void  callback_function_depth(const sensor_msgs::Image::ConstPtr  image_data)
{
   Mat temp;
   cv_bridge::CvImageConstPtr pCvImage;// 声明一个CvImage指针的实例
   pCvImage = cv_bridge::toCvShare(image_data, image_data->encoding);//将ROS消息中的图象信息提取，生成新cv类型的图象，复制给CvImage指针
   pCvImage->image.copyTo(temp);//由于此depth图32FC1格式数据分布在4,5之间，所以需要转换

   double minv = 0.0, maxv = 0.0;//maxv就是zfar的值
   minMaxIdx(temp,&minv,&maxv);//获取temp的最大最小值
   cout << "Mat minv = " << minv <<"type:"<<temp.type()<<"channel"<<temp.channels()<< endl;
   cout << "Mat maxv = " << maxv << endl;
    #pragma omp parallel for
    for(int i=0;i<temp.rows;i++)//ros输出的深度图数据是32fc1格式，数值是m为单位，所以需要转换成mm单位
    {
        for(int j=0;j<temp.cols;j++)
        {
            if((float)temp.at<float>(i,j)==maxv)
                temp.ptr<float>(i)[j]=0;
        }
    }
	temp.convertTo(depth, CV_16UC1, 1000);//src.convertTo(dst, type, scale, shift)
    //minMaxIdx(depth,&minv,&maxv);
	//depth.convertTo(depth1, CV_8UC1, 255.0/(maxv*1000.0));
	//imshow("a", depth);
	//cout << "temp" << temp << endl;//cv的格式化输出

//   cout<<"the  depth heigh"<<image_data->height<<endl;
//   cout<<"the depth width"<<image_data->width<<endl;
//   cout<<"the depth step"<<image_data->step<<endl;
//   cout<<"listen ...."<<endl;

   //dispDepth(depth, 1000.0f);
   successed_flag2=1;
   //imshow("Matdepth",depth/256);
  // cv::waitKey(0);
}
