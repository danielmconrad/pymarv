#!/usr/bin/python

import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

MOTOR_INDEXES = {
  "LEFT": [2, 3],
  "RIGHT": [1, 4]
}

class Motors:
  def __init__(self):
    self.__add_motors()
    atexit.register(self.__turn_all_motors_off)


  # Public

  def tank_move(self, left_magnitude, right_magnitude):
    self.set_motors_magnitude(self.left_motors, left_magnitude)
    self.set_motors_magnitude(self.right_motors, right_magnitude)

  def stop(self):
    self.__turn_all_motors_off()


  # Private

  def __add_motors(self):
    self.motors = []
    self.left_motors = []
    self.right_motors = []

    motors = Adafruit_MotorHAT(addr=0x60)

    for i in MOTOR_INDEXES["LEFT"]:
      motor = motors.getMotor(i)
      self.motors.append(motor)
      self.left_motors.append(motor)

    for i in MOTOR_INDEXES["RIGHT"]:
      motor = motors.getMotor(i)
      self.motors.append(motor)
      self.right_motors.append(motor)

  def set_motors_magnitude(self, motors, magnitude):
    for motor in motors:
      self.set_motor_magnitude(motor, magnitude)

  def set_motor_magnitude(self, motor, magnitude):
    actual_speed = min(255, int(abs(magnitude) * 255))

    if magnitude < 0:
      self.__set_motor_forward(motor)
      self.__set_motor_speed(motor, actual_speed)
    elif magnitude > 0:
      self.__set_motor_backward(motor)
      self.__set_motor_speed(motor, actual_speed)
    else:
      self.__set_motor_speed(motor, 0)


  # Off
  def __turn_all_motors_off(self):
    self.__turn_motors_off(self.motors)

  def __turn_motors_off(self, motors):
    for motor in motors:
      self.__turn_motor_off(motor)

  def __turn_motor_off(self, motor):
    motor.run(Adafruit_MotorHAT.RELEASE)

  # Forward
  def __set_motors_forward(self, motors):
    for motor in motors:
      self.__set_motor_forward(motor)

  def __set_motor_forward(self, motor):
    motor.run(Adafruit_MotorHAT.FORWARD)

  # Backward
  def __set_motors_backward(self, motors):
    for motor in motors:
      self.__set_motor_backward(motor)

  def __set_motor_backward(self, motor):
    motor.run(Adafruit_MotorHAT.BACKWARD)

  # Speed
  def __set_motors_speed(self, motors, speed):
    for motor in motors:
      self.__set_motor_speed(motor, speed)

  def __set_motor_speed(self, motor, speed):
    motor.setSpeed(speed)
