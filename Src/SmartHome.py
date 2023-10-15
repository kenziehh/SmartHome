
import time

from AutomaticDevice import AutomaticControlledDevice

class Smarthome:
    def __init__(self):
        self.rooms = []
        self.current_condition = {
            "temperature": 25,  # Initial temperature
            "time": (0, 0)      # Initial time (hour, minute)
        

        }

    def add_room(self, room):
        self.rooms.append(room)

    def simulate_24_hours(self):
        for hour in range(24):
            for minute in range(60):
                self.current_condition["time"] = (hour, minute)
                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                print(f"Time: {hour:02d}:{minute:02d}, Temperature: int({self.current_condition['temperature']}°C), Total Energy Consumption: {total_energy_consumption} Watt")

                # Simulate changes in temperature (You can customize this part)
                if 9 <= hour < 17:
                    self.current_condition["temperature"] += 0.1 
                else:
                    pass

                time.sleep(0.01)  # Simulate 1 minute delay
    
    