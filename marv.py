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
      # os.system('clear')
      pass
      # print(json.dumps(state, sort_keys=True, indent=2))

marv = Marv()
marv.start()
