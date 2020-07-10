import picamera

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class CameraManager(object):

    def __init__(self):
        self.camera = None

    def open_camera(self):
        self.close_camera()
        self.camera = picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30)

    def close_camera(self):
        if self.camera is not None and not self.camera.closed:
            self.camera.close()
