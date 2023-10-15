
import time

from AutomaticDevice import AutomaticDevice

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