import evdev

class PS4Controller:
  def __init__(self):
    self.controller = self.get_controller()
    self.print_capabilities()

  def get_controller(self):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
      if "DUALSHOCK" in device.name:
        return evdev.InputDevice(device.fn)

  def print_capabilities(self):
    print(self.controller.capabilities(verbose=True))

  def listen(self):
    for event in self.controller.read_loop():
      self.handle_event(event)

  def handle_event(self, event):
    print(evdev.util.categorize(event))

  # if event.type == evdev.ecodes.EV_KEY:
  #   print(evdev.util.categorize(event))

controller = PS4Controller()
controller.listen()
