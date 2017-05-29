#!/usr/bin/python

import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

motors = Adafruit_MotorHAT(addr=0x60)

class Motors:
  def __init__(self):
    self.motors = []
    self.left_motors = []
    self.right_motors = []

    self.__add_motors()

    atexit.register(self.__turn_off_motors)


  # Public

  def move(self, angle, magnitude):
    print(angle, magnitude)


  # Private

  def __add_motors(self):
    for i in range(1, 3):
      motor = motors.getMotor(i)
      self.motors.append(motor)
      self.left_motors.append(motor)

    for i in range(3, 5):
      motor = motors.getMotor(i)
      self.motors.append(motor)
      self.right_motors.append(motor)

  def __turn_off_motors(self):
    map(self.__turn_off_motor, self.motors)

  def __turn_off_motor(self, motor):
    motor.run(Adafruit_MotorHAT.RELEASE)



  # def setDirection(forwardBackward):
  #   actualSpeed = int(abs(forwardBackward) * 255)

  #   if forwardBackward < 0:
  #     setForward()
  #     setSpeed(actualSpeed)
  #   elif forwardBackward > 0:
  #     setBackward()
  #     setSpeed(actualSpeed)
  #   else:
  #     __turn_off_motors()

  # def setSpeed(speed):
  #   for i in range(1, 5):
  #     motors.getMotor(i).setSpeed(speed)

  # def __turn_off_motors():
  #   for i in range(1, 5):
  #     motors.getMotor(i).run(Adafruit_MotorHAT.RELEASE)

  # def setForward():
  #   for i in range(1, 5):
  #     motors.getMotor(i).run(Adafruit_MotorHAT.FORWARD)

  # def setBackward():
  #   for i in range(1, 5):
  #     motors.getMotor(i).run(Adafruit_MotorHAT.BACKWARD)
