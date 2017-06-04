import evdev
import math

from evdev import ecodes
from evdev.util import categorize, event_factory
from evdev.events import KeyEvent, AbsEvent, SynEvent

EMPTY_STATE = {
  "X": {}
}

class Steam:
  def __init__(self):
    self.state = EMPTY_STATE
    self.controller = self.__get_controller()


  def __get_controller(self):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
      if "Valve Software Steam" in device.name:
        return evdev.InputDevice(device.fn)

  # Public

  def is_connected(self):
    if self.controller is None:
      return False
    else:
      return True

  def print_capabilities(self):
    print(self.controller.capabilities(verbose=True))

  def listen(self):
    for event in self.controller.read_loop():
      self.__handle_event(event)

      if type(evdev.util.categorize(event)) is SynEvent:
        yield self.state

  # # Private

  def __handle_event(self, event):
    categorized_event = evdev.util.categorize(event)
