import picamera

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class CameraManager(object):

    def __init__(self):
        self.camera = None

    def open_camera(self):
        self.camera = picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30)

    def close_camera(self):
        self.camera.close()