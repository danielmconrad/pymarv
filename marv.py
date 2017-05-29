#!/usr/bin/python

import atexit
import controller
import motors
import os
import json

class Marv:
  def __init__(self):
    self.motors = motors.Motors()
    self.controller = controller.PS4Controller()

  def start(self):
    for state in self.controller.listen():
      angle = state["LEFT_ANALOG"]["angle"]
      magnitude = state["LEFT_ANALOG"]["magnitude"]
      self.motors.move(angle, magnitude)

marv = Marv()
marv.start()
