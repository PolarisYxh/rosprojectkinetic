import socket
from PIL import Image
import struct
from cv_bridge import CvBridge,CvBridgeError
import cv2
import numpy as np
class client:
    def __init__(self,server_ip,server_port):
        self.host_content=server_ip
        self.port_content=server_port

    def get_rgbd(self):
        host = self.host_content
        port = self.port_content
        s = socket.socket()
        s.connect((host, int(port)))
        self.num=0.000000
        #get intrinsic
        s.send('intrinsic'.encode('utf-8'))
        #s.send(bytes('intrinsic', encoding='utf-8'))
        str1=s.recv(60)#60个字节
        data = bytearray(str1)
        headIndex = data.find(b'\xff\xaa\xff\xab')
        if headIndex == 0:
            width,height= struct.unpack('<ii',str1[4:12])
            pMtr=struct.unpack('%df'%((len(str1)-12)/4),str1[12:])
            print(height)
            print(width)
            #print(pMtr)
            #get rgbd
            while True:
                #s.send(bytes('rgbd', encoding='utf-8'))
                str1 = s.recv(12)
                # head check
                data = bytearray(str1)
                headIndex = data.find(b'\xff\xaa\xff\xaa')
                if headIndex == 0:
                    rgbLen,depthLen = struct.unpack('<ii',str1[4:12])
                    curSize = 0
                    allData = b''
                    while curSize < rgbLen:
                            data = s.recv(1024)
                            allData += data
                            curSize += len(data)
                    rgbData=allData[0:]
                    
                    curSize = 0
                    allData = b''
                    while curSize < depthLen:
                            data = s.recv(1024)
                            allData += data
                            curSize += len(data)
                    depthData = allData[0:]

                    # bytes to PIL.Image
                    img = Image.frombuffer('RGB', (width, height), rgbData,'raw', 'BGR', 0, 1)
                    # top and down flip
                    #img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    #save
                    name='%f' %self.num
                    print(name)
                    #img.show()
                    img.save('/home/yxh/'+name+'.jpg',format='JPEG')
                    #bytes转float32，好几种方法
                    dtype = np.dtype('float32')
                    dtype = dtype.newbyteorder('<')
                    image = np.ndarray(shape=(height,width),dtype=dtype, buffer=depthData)
                    image = np.nan_to_num(image)
                    # #法2
                    # image=struct.unpack('<%df'%(depthLen/4), depthData)
                    # #法3
                    # image=np.frombuffer(depthData, dtype='float32')
                    # image=image.reshape((width,height))
                    #image = cv2.imdecode(image, cv2.CV_32FC1)
                    #cv2.imshow('URL2Image',image)
                    cv2.imwrite('/home/yxh/'+name+'.png',image)
                    self.num+=0.000001
                    # qimage = QImage(img_conv, 640, 480, QImage.Format_RGB888)
                    # pixmap = QPixmap.fromImage(qimage)
                    # #
                    # self.dis_update.emit(pixmap)

if __name__ == "__main__":
    rgbdclient=client('localhost','9090')
    rgbdclient.get_rgbd()