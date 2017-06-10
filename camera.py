from picamera import PiCamera
from time import sleep


class Camera:
  def __init__(self):
    self.camera = PiCamera()

  def capture(self):
    camera.start_preview()
    sleep(2)
    self.camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
