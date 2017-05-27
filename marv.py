#!/usr/bin/python

import time
import atexit
import pprint
import pygame
import os
import sys

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

# Disable video mode
import pygame.display
import pygame.transform






# create a default object, no changes to I2C address or frequency
motors = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!

def setDirection(forwardBackward, leftRight):
  actualSpeed = int(abs(forwardBackward) * 255)

  if forwardBackward < 0:
    setForward()
    setSpeed(actualSpeed)
  elif forwardBackward > 0:
    setBackward()
    setSpeed(actualSpeed)
  else:
    turnOffMotors()

def setSpeed(speed):
  for i in range(1, 5):
    motors.getMotor(i).setSpeed(speed)

def turnOffMotors():
  for i in range(1, 5):
    motors.getMotor(i).run(Adafruit_MotorHAT.RELEASE)

def setForward():
  for i in range(1, 5):
    motors.getMotor(i).run(Adafruit_MotorHAT.FORWARD)

def setBackward():
  for i in range(1, 5):
    motors.getMotor(i).run(Adafruit_MotorHAT.BACKWARD)

atexit.register(turnOffMotors)

class PS4Controller(object):
  controller = None
  axis_data = None
  button_data = None
  hat_data = None

  def init(self):
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    pygame.joystick.init()
    pygame.display.init()

    # screen = pygame.display.set_mode((1,1))

    self.controller = pygame.joystick.Joystick(0)
    self.controller.init()

    self.axis_data = {
      'forwardBackward': 0,
      'leftRight': 0
    }

    self.axes = [
      'horizontal',
      'vertical',
      'leftRight',
      'leftTrigger',
      'rightTrigger',
      'forwardBackward'
    ]

    self.button_data = {}
    for i in range(self.controller.get_numbuttons()):
      self.button_data[i] = False

    self.hat_data = {}

    for i in range(self.controller.get_numhats()):
      self.hat_data[i] = (0, 0)

  def listen(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
          self.axis_data[self.axes[event.axis]] = round(event.value, 2)

        elif event.type == pygame.JOYBUTTONDOWN:
          self.button_data[event.button] = True

        elif event.type == pygame.JOYBUTTONUP:
          self.button_data[event.button] = False

        elif event.type == pygame.JOYHATMOTION:
          self.hat_data[event.hat] = event.value

        os.system('clear')

        #pprint.pprint(self.button_data)
        pprint.pprint(self.axis_data)
        #pprint.pprint(self.hat_data)
        ##pprint.pprint(self.axis_data)

      setDirection(self.axis_data['forwardBackward'], self.axis_data['leftRight'])

ps4 = PS4Controller()
ps4.init()
ps4.listen()


# hi george.
