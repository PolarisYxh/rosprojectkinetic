#!/usr/bin/env python2
#coding:utf-8

import rospy
import cv2
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge,CvBridgeError
import socket
import threading
import sys                                                                  
import signal
import struct#used for net pack 

class Node:
    def __init__(self):
        self.flag1=False
        self.flag2=False
        self.num1=0.000000
        self.intrinsic=None
        self.rgbtopic=rospy.Subscriber('/camera/rgb/image_raw', Image, self.rgbcallback)
        self.depthtopic=rospy.Subscriber('/camera/depth/image_raw',Image,self.depthcallback)
        self.intrintopic=rospy.Subscriber('/camera/rgb/camera_info',CameraInfo,self.intrinsic_callback_once)
        #child thread to run server
        #t1 = threading.Thread(target=self.socket_server)
        #t1.setDaemon(True)#set daemon for ctrl c to quit
        #t1.start()
    def quit(self,signum, frame):
        sys.exit()
    def Int_ToBytes(self,n,length):#big
        return bytes('%%0%dx' % (length << 1) % n).decode('hex')[-length:]
    def socket_server(self):
        signal.signal(signal.SIGINT, self.quit)                                
        signal.signal(signal.SIGTERM, self.quit)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        host = socket.gethostname()  # 获取本地主机名
        port = 12345  # 设置端口
        s.bind(('localhost',9090))  # 绑定端口
        print('localhost'+" server open")
        s.listen(5)
        while True:
            try:
                print('start accept')
                c, addr = s.accept()  # 建立客户端连接,阻塞等待
                print("连接地址:" + str(addr))
                # 先获取客户端发送过来的请求
                rec_data = c.recv(64)
                #rec_data = str(rec_data, encoding='utf-8')
                rec_data = rec_data.decode()
                while True:
                    # 是返回rgbd or intrinsic
                    if rec_data == "rgbd" and self.flag1 and self.flag2:
                        print('trans '+rec_data)
                        self.flag1=False
                        self.flag2=False
                        arrBuf = bytearray(b'\xff\xaa\xff\xaa')
                        rgbBytes = self.rgb_image.tobytes()
                        
                        depthBytes = self.depth_image.tobytes()
                        # 图片大小
                        rgbSize = len(rgbBytes)#rgb one pixel 1 byte char
                        depthSize = len(depthBytes)#depth one pixel 4 bytes double
                        # 数据体长度 = guid大小(固定) + 图片大小
                        rgbdatalen = rgbSize
                        depthdatalen = depthSize
                        # 组合数据包
                        arrBuf += struct.pack('<i',rgbdatalen)
                        arrBuf += struct.pack('<i',depthdatalen)
                        c.sendall(arrBuf)
                        #print(rgbdatalen)
                        #arrBuf += struct.pack('<%di'%rgbdatalen,* rgbBytes)
                        arrBuf=rgbBytes
                        #print(len(arrBuf))
                        print(depthdatalen)
                        #arrBuf += struct.pack('<%di'%depthdatalen,* depthBytes)
                        arrBuf+=depthBytes
                        print(len(arrBuf))
                        c.sendall(arrBuf)
                    # 用来返回口腔坐标信息， 只需要发送图像的可忽略
                    elif rec_data == "intrinsic" and self.intrinsic!=None:
                        print(rec_data)
                        intrindata=self.intrinsic
                        prjmtr=list(intrindata.P)
                        print(len(prjmtr))
                        width=intrindata.width
                        height=intrindata.height
                        send_data=b'\xff\xaa\xff\xab'+struct.pack('<ii%df'%len(prjmtr),width,height,* prjmtr)
                        print(len(send_data))
                        #send_data += self.intrinsic
                        c.sendall(send_data)#bytes是编码，str是解码函数
                        rec_data = "rgbd"
                c.close()
            except Exception as e:
                print("exception:")
                print(e.args)
                s.close()
                return
        s.close()

    def rgbcallback(self,data):
        bridge = CvBridge()
        self.rgb_image = bridge.imgmsg_to_cv2(data,'passthrough')#convert data to numpy
        #cv2.imshow("rgb",rgb_image)
        self.flag1=True
        
    def depthcallback(self,data):    
        bridge = CvBridge()
        self.depth_image = bridge.imgmsg_to_cv2(data,'passthrough')
        #print(data.encoding)  32FC1
        #print(data.is_bigendian)  小端传输
        #cv2.imshow("depth",depth_image)
        self.flag2=True
    def intrinsic_callback_once(self,data):
        self.intrinsic=data
        #print(data)
        self.intrintopic.unregister()
    def save(self):
        while not rospy.is_shutdown():
            if self.flag1 and self.flag2:
                self.flag1=False
                self.flag2=False
                s = '%f' %self.num1
                rgb_name='/home/yxh/RGBD_1/rgb/'+s+'.jpg'
                depth_name='/home/yxh/RGBD_1/depth/'+s+'.png'
                cv2.imwrite(rgb_name,self.rgb_image)
                print(rgb_name)
                cv2.imwrite(depth_name,self.depth_image)
                print(depth_name)
                self.num1+=0.000001
            if self.intrinsic!=None:#保存intrinsic
                print(self.intrinsic)
                self.intrinsic=None
                #info_name
if __name__ == '__main__':
    rospy.init_node('getImage',anonymous = True)
    my_node = Node()
    my_node.socket_server()

    
#     # t1 = threading.Thread(target=socket_server)
#     # t1.start()
# flag1=False
# flag2=False
# rgb_image=None
# depth_image=None
# def socket_server():
#     s = socket.socket()  # 创建 socket 对象
#     host = socket.gethostname()  # 获取本地主机名
#     port = 60000  # 设置端口
#     s.bind((host, port))  # 绑定端口
#     print("服务端开启")
#     s.listen(5)
#     while 1:
#         try:
#             c, addr = s.accept()  # 建立客户端连接
#             print("连接地址:" + str(addr))
#             send_data = get_bytes()
#             # send函数发送的是bytes格式的数据
#             c.send(send_data)
#             c.close()
#         except Exception as e:
#             print("远程主机强制关闭连接")
#             print(e.args)
# def rgbcallback(data):
#     global flag1,rgb_image
#     bridge = CvBridge()
#     rgb_image = bridge.imgmsg_to_cv2(data,'passthrough')
#     #cv2.imshow("rgb",rgb_image)
#     flag1=True
    
# def depthcallback(data):
#     global flag2,depth_image   
#     bridge = CvBridge()
#     depth_image = bridge.imgmsg_to_cv2(data,'passthrough')
#     #cv2.imshow("depth",depth_image)
#     flag2=True
    
# if __name__ == '__main__':
#     rospy.init_node('getImage',anonymous = True)
#     rospy.Subscriber('/camera/rgb/image_raw', Image, rgbcallback)
#     rospy.Subscriber('/camera/depth/image_raw',Image,depthcallback)
    
#     num1=0.000000
#     #global flag1,flag2
#     while not rospy.is_shutdown():
#         if flag1 and flag2:
#             flag1=False
#             flag2=False
#             s = '%f' %num1
#             rgb_name='/home/yxh/RGBD_1/rgb/'+s+'.jpg'#'./rgb/'+
#             depth_name='/home/yxh/RGBD_1/depth/'+s+'.png'#'./depth/'+
#             cv2.imwrite(rgb_name,rgb_image)
#             print(rgb_name)
#             cv2.imwrite(depth_name,depth_image)
#             print(depth_name)
#             num1+=0.000001

    
    # t1 = threading.Thread(target=socket_server)
    # t1.start()