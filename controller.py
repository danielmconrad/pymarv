import evdev
import os

from evdev import ecodes
from evdev.util import categorize, event_factory
from evdev.events import KeyEvent, AbsEvent, SynEvent

PRETTY_MAP = {
  'BTN_MODE': 'PLAYSTATION',
  'BTN_WEST': 'L1',
  'BTN_TL': 'L2',
  'BTN_Z': 'R1',
  'BTN_TR': 'R2',
  'BTN_TL2': 'SHARE',
  'BTN_THUMBL': 'TOUCHPAD',
  'BTN_TR2': 'OPTIONS',
  'BTN_SELECT': 'LEFT_ANALOG',
  'BTN_START': 'RIGHT_ANALOG',
  'BTN_NORTH': 'TRIANGLE',
  'BTN_C': 'CIRCLE',
  'BTN_B': 'CROSS',
  'BTN_A': 'SQUARE',
  'ABS_RX': 'L2',
  'ABS_RY': 'R2',
  'ABS_HAT0Y': 'DPAD_VERTICAL',
  'ABS_HAT0X': 'DPAD_HORIZONTAL',
  'ABS_Y': 'LEFT_ANALOG_VERTICAL',
  'ABS_X': 'LEFT_ANALOG_HORIZONTAL',
  'ABS_RZ': 'RIGHT_ANALOG_VERTICAL',
  'ABS_Z': 'RIGHT_ANALOG_HORIZONTAL'
}

class PS4ControllerState:
  def __init__(self):
    self.state = {
      'PLAYSTATION': {},
      'L1': {},
      'L2': {},
      'R1': {},
      'R2': {},
      'SHARE': {},
      'TOUCHPAD': {},
      'OPTIONS': {},
      'LEFT_ANALOG': {},
      'RIGHT_ANALOG': {},
      'TRIANGLE': {},
      'CIRCLE': {},
      'CROSS': {},
      'SQUARE': {},
      'L2': {},
      'R2': {},
      'DPAD_VERTICAL': {},
      'DPAD_HORIZONTAL': {},
      'LEFT_ANALOG_VERTICAL': {},
      'LEFT_ANALOG_HORIZONTAL': {},
      'RIGHT_ANALOG_VERTICAL': {},
      'RIGHT_ANALOG_HORIZONTAL': {}
    }

  def add_axis_value(self, code, value):
    self.__create_or_extend_button(code)
    self.state[code]["value"] = value

  def add_key_state(self, code, state):
    self.__create_or_extend_button(code)
    self.state[code]["state"] = state

  def __create_or_extend_button(self, code):
    if code not in self.state:
      self.state[code] = {}

class PS4Controller:
  def __init__(self):
    self.controller = self.__get_controller()

  def __get_controller(self):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
      if "DUALSHOCK®4" in device.name:
        return evdev.InputDevice(device.fn)

    raise ValueError("Unable to find a connected PS4 controller.")

  # Public

  def listen(self):
    controller_state = PS4ControllerState()

    for event in self.controller.read_loop():
      should_yield = self.__handle_event(event, controller_state)

      print(str(should_yield))

      if should_yield:
        yield controller_state
        controller_state = PS4ControllerState()

  def read(self):
    controller_state = PS4ControllerState()

    for event in self.controller.read():
      self.__handle_event(event, controller_state)

    return controller_state

  # Private

  def __handle_event(self, event, controller_state):
    categorized_event = evdev.util.categorize(event)

    if type(categorized_event) is KeyEvent:
      [code, state] = self.__get_key_event(categorized_event)
      controller_state.add_key_state(code, state)
      return False

    if type(categorized_event) is AbsEvent:
      [code, value] = self.__get_abs_event(event)
      controller_state.add_axis_value(code, value)
      return False

    if type(categorized_event) is SynEvent:
      return True

  def __get_key_event(self, event):
    pretty_code = self.__get_pretty_code(event.keycode)
    return [pretty_code, event.keystate]

  def __get_abs_event(self, event):
    pretty_code = self.__get_pretty_code(ecodes.ABS[event.code])
    return [pretty_code, event.value]

  def __get_pretty_code(self, code):
    if isinstance(code, list):
      code = code[0]
    return PRETTY_MAP[code]


# controller = PS4Controller()
# controller_state = controller.read()
# print(controller_state.state)

for controller_state in controller.listen():
  os.system('clear')
  print(controller_state.state)
