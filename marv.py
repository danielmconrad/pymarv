#!/usr/bin/python

import atexit
import controller
import motors
import time

class Marv:
  def __init__(self):
    self.motors = motors.Motors()
    self.controller = controller.PS4Controller()
    atexit.register(self.__stop_devices)

  def start(self):
    for state in self.controller.listen():
      left = state["LEFT_ANALOG_VERTICAL"]["magnitude"]
      right = state["RIGHT_ANALOG_VERTICAL"]["magnitude"]

      left = self.__maximize_magnitude(left)
      right = self.__maximize_magnitude(right)

      self.motors.tank_move(left, right)

  def __maximize_magnitude(self, magnitude):
    if magnitude >= -0.5 and magnitude < 0.5:
      return 0
    elif magnitude < 0:
      return -1
    else:
      return 1

  def __stop_devices(self):
    self.motors.stop()
    self.controller.free()

  def __test_motors(self):
    self.motors.tank_move(1, 1)
    time.sleep(1)
    self.motors.tank_move(-1, 1)
    time.sleep(1)
    self.motors.tank_move(-1, -1)
    time.sleep(1)
    self.motors.tank_move(1, -1)
    time.sleep(1)
    self.motors.stop()

marv = Marv()
marv.start()
