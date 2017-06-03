from controller.dualshock import Dualshock
from controller.steam import Steam

def get_any_controller():
  dualshock = Dualshock()
  if dualshock.is_connected():
    return dualshock

  steam = Steam()
  if steam.is_connected():
    return steam

  raise ValueError("Unable to find a connected controller.")
