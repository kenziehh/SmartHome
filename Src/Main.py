import time

from AutomaticDevice import AutomaticDevice
from ElectronicDevice import ElectronicDevice
from Room import Room
from SmartHome import Smarthome

if __name__ == "__main__":
    # Create electronic devices
    ac = AutomaticDevice("Air Conditioner", 800, lambda cond: cond["temperature"] > 30, lambda cond: cond["temperature"] <= 20)
    lamp = AutomaticDevice("Lamp", 50, lambda cond: cond["time"][0] < 6 or cond["time"][0] >= 18, lambda cond: False)
    tv = ElectronicDevice("Television", 100)
    refridgerator = ElectronicDevice("Refridgerator", 150)
    # Create rooms and add devices to them
    living_room = Room("Living Room")
    living_room.add_device(tv, 1)
    bedroom = Room("Bedroom")
    bedroom.add_device(ac, 1)
    bedroom.add_device(lamp, 1)
    
    terrace = Room("Terracce")
    terrace.add_device(lamp, 2)
    
    bathroom = Room("Bathroom")
    bathroom.add_device(lamp, 1)
    # Create and simulate the smart home
    smart_home = Smarthome()
    # smart_home.add_room(living_room)
    smart_home.add_room(bedroom)
    smart_home.add_room(terrace)
    smart_home.add_room(bathroom)
    
    smart_home.simulate_24_hours()
