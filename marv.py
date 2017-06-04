#!/usr/bin/python

import controller
import motors
import time

class Marv:
  def __init__(self):
    self.motors = motors.Motors()
    self.controller = controller.get_any_controller()
    self.controller.print_capabilities()

    self.last_left = None
    self.last_right = None

  def start(self):
    for state in self.controller.listen():
      self.__handle_tank_move(state)

  def __handle_tank_move(self, state):
    left = state["LEFT_ANALOG_VERTICAL"]["magnitude"]
    right = state["RIGHT_ANALOG_VERTICAL"]["magnitude"]

    left = self.__adjust_magnitude(left)
    right = self.__adjust_magnitude(right)

    if left != self.last_left or right != self.last_right:
      self.motors.tank_move(left, right)
      self.last_left = left
      self.last_right = right

  def __adjust_magnitude(self, magnitude):
    if -0.3 < magnitude and magnitude < 0.3:
      return 0
    else:
      return magnitude * 1.2

marv = Marv()
marv.start()
