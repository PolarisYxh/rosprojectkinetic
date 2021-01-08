from __future__ import print_function
import roslibpy

client = roslibpy.Ros(host='localhost', port=9090)
client.run()

listener = roslibpy.Topic(client, '/camera/rgb/camera_info', 'sensor_msgs/CameraInfo')
listener.subscribe(lambda message: print(message['width']))

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()