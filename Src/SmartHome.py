
import time

from AutomaticDevice import AutomaticDevice
     
class Smarthome:
    def __init__(self):
        self.rooms = []
        self.current_condition = {
            "temperature": 25,  # Initial temperature
            "time": (0, 0)      # Initial time (hour, minute)
        }
        self.ac_active = False  # Tambahkan atribut ini untuk melacak status AC
        self.lamp_active = False  # Tambahkan atribut ini untuk melacak status lampu


    def add_room(self, room):
        self.rooms.append(room)

    #jangan dihapus!!
    
    # def simulate_24_hours(self):
    #     for hour in range(24):
    #         for minute in range(60):
    #             self.current_condition["time"] = (hour, minute)
    #             # Simulate changes in temperature
    #             if 9 <= hour < 14:
    #                 if self.current_condition["temperature"] < 30 and not self.ac_active:
    #                     self.current_condition["temperature"] += 0.083
    #                     if self.current_condition["temperature"] >= 30:
    #                         self.ac_active = True  # Aktifkan AC saat suhu mencapai 30 derajat
    #                 elif self.ac_active:
    #                     self.current_condition["temperature"] -= 0.083
    #                     if self.current_condition["temperature"] <= 20:
    #                         self.ac_active = False  # Matikan AC saat suhu mencapai 20 derajat
    #             elif 14 <= hour <=18 and self.current_condition["temperature"] > 25:
    #                 self.current_condition["temperature"] -= 0.083
    #                 self.ac_active = False  # Pastikan AC mati di luar jam 9-14
    #             else:
    #                 self.current_condition["temperature"] -= 0
    #                 self.ac_active = False  # Pastikan AC mati di luar jam 9-14
    #             if 5<= hour <18:
    #                 self.lamp_active = False
    #             elif 18<= hour <5:
    #                 self.lamp_active = True
    #             for room in self.rooms:
    #                 for device, quantity in room.devices.items():
    #                     if isinstance(device, AutomaticDevice) and device.name == "Lamp":
    #                         if hour < 5 or hour >= 18:
    #                             device.active = True  # Aktifkan lampu saat jam 18:00
    #                         elif hour >= 5 and hour < 18:
    #                             device.active = False  # Matikan lampu saat jam 5:00
    #             for room in self.rooms:
    #                 room.calculate_total_energy_consumption(self.current_condition)
    #             total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
    #             print(f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
    #             time.sleep(0.01)  # Simulate 1 minute delay
    
    def control_ac(self):
        if 9 <= self.current_condition["time"][0] < 14:
            if self.current_condition["temperature"] < 30 and not self.ac_active:
                self.current_condition["temperature"] += 0.083
                if self.current_condition["temperature"] >= 30:
                    self.ac_active = True  # Aktifkan AC saat suhu mencapai 30 derajat
            elif self.ac_active:
                self.current_condition["temperature"] -= 0.083
                if self.current_condition["temperature"] <= 20:
                    self.ac_active = False  # Matikan AC saat suhu mencapai 20 derajat
        elif 14 <= self.current_condition["time"][0] <= 18 and self.current_condition["temperature"] > 25:
            self.current_condition["temperature"] -= 0.083
            self.ac_active = False  # Pastikan AC mati di luar jam 9-14
        else:
            self.current_condition["temperature"] -= 0
            self.ac_active = False  # Pastikan AC mati di luar jam 9-14
            
    def control_lamp(self):
        hour = self.current_condition["time"][0]
        for room in self.rooms:
            for device, quantity in room.devices.items():
                if isinstance(device, AutomaticDevice) and device.name == "Lamp":
                    if hour < 5 or hour >= 18:
                        device.active = True  # Aktifkan lampu saat jam 18:00
                    elif hour >= 5 and hour < 18:
                        device.active = False  # Matikan lampu saat jam 5:00
                        
    
    def simulate_24_hours(self):
        for hour in range(24):
            for minute in range(60):
                self.current_condition["time"] = (hour, minute)
                self.control_ac()
                
                self.control_lamp()
                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                print(f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
                time.sleep(0.01)  # Simulate 1 minute delay
                