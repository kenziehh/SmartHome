import time

class ElectronicDevice:
    def __init__(self, name, energy_cost):
        self.name = name
        self.energy_cost = energy_cost  # Watt

    def get_total_energy_consumption(self, quantity):
        return self.energy_cost * quantity

class AutomaticControlledDevice(ElectronicDevice):
    def __init__(self, name, energy_cost, control_condition, turn_off_condition):
        super().__init__(name, energy_cost)
        self.control_condition = control_condition  # Function to check when to turn on
        self.turn_off_condition = turn_off_condition  # Function to check when to turn off
        self.active = False

    def is_active(self, current_condition):
        if self.active and self.turn_off_condition(current_condition):
            self.active = False
        elif not self.active and self.control_condition(current_condition):
            self.active = True
        return self.active

class Room:
    def __init__(self, name):
        self.name = name
        self.devices = {}
        self.total_energy_consumption = 0

    def add_device(self, device, quantity):
        self.devices[device] = quantity

    def calculate_total_energy_consumption(self, current_condition):
        total_consumption = 0
        for device, quantity in self.devices.items():
            if isinstance(device, AutomaticControlledDevice) and device.is_active(current_condition):
                total_consumption += device.get_total_energy_consumption(quantity)
            elif not isinstance(device, AutomaticControlledDevice):
                total_consumption += device.get_total_energy_consumption(quantity)
        self.total_energy_consumption = total_consumption
        
class Smarthome:
    def __init__(self):
        self.rooms = []
        self.current_condition = {
            "temperature": 25,  # Initial temperature
            "time": (0, 0)      # Initial time (hour, minute)
        }
        self.ac_active = False  # Tambahkan atribut ini untuk melacak status AC

    # ... (kode lainnya tetap sama)
        self.lamp_active = False  # Tambahkan atribut ini untuk melacak status lampu


    def add_room(self, room):
        self.rooms.append(room)

    # def control_ac(self):
    #     if self.current_condition["temperature"] < 30 and not self.ac_active:
    #         self.current_condition["temperature"] += 0.083
    #         if self.current_condition["temperature"] >= 30:
    #             self.ac_active = True  # Aktifkan AC saat suhu mencapai 30 derajat
    #     elif self.ac_active:
    #         self.current_condition["temperature"] -= 0.083
    #         if self.current_condition["temperature"] <= 20:
    #             self.ac_active = False  # Matikan AC saat suhu mencapai 20 derajat
    #         else:
    #             self.current_condition["temperature"] -= 0
    #             self.ac_active = False  # Pastikan AC mati di luar jam 9-14
                
    
    def simulate_24_hours(self):
        for hour in range(24):
            for minute in range(60):
                self.current_condition["time"] = (hour, minute)
                # Simulate changes in temperature
                if 9 <= hour < 14:
                    if self.current_condition["temperature"] < 30 and not self.ac_active:
                        self.current_condition["temperature"] += 0.083
                        if self.current_condition["temperature"] >= 30:
                            self.ac_active = True  # Aktifkan AC saat suhu mencapai 30 derajat
                    elif self.ac_active:
                        self.current_condition["temperature"] -= 0.083
                        if self.current_condition["temperature"] <= 20:
                            self.ac_active = False  # Matikan AC saat suhu mencapai 20 derajat
                elif 14 <= hour <=18 and self.current_condition["temperature"] > 25:
                    self.current_condition["temperature"] -= 0.083
                    self.ac_active = False  # Pastikan AC mati di luar jam 9-14
                else:
                    self.current_condition["temperature"] -= 0
                    self.ac_active = False  # Pastikan AC mati di luar jam 9-14
                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                print(f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
                time.sleep(0.01)  # Simulate 1 minute delay


if __name__ == "__main__":
    # Create electronic devices
    ac = AutomaticControlledDevice("Air Conditioner", 1500, lambda cond: cond["temperature"] > 30, lambda cond: cond["temperature"] <= 20)
    lamp = AutomaticControlledDevice("Lamp", 100, lambda cond: cond["time"][0] < 6 or cond["time"][0] >= 18, lambda cond: False)
    tv = ElectronicDevice("Television", 300)

    # Create rooms and add devices to them
    living_room = Room("Living Room")
    living_room.add_device(ac, 1)
    # living_room.add_device(tv, 1)

    bedroom = Room("Bedroom")
    bedroom.add_device(lamp, 1)

    # Create and simulate the smart home
    smart_home = Smarthome()
    smart_home.add_room(living_room)
    smart_home.add_room(bedroom)

    smart_home.simulate_24_hours()
