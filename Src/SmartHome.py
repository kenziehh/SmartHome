import numpy as np
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
        self.total_energy_consumption_day = 0

    def add_room(self, room):
        self.rooms.append(room)

    def simulate_temperature_with_noise(self):
            # Simulasi pengaruh lingkungan
        if self.ac_active:
            # Jika AC aktif, suhu akan turun dengan lebih cepat
            self.current_condition["temperature"] -= 0.08
        else:
            # Pengaruh alami, misalnya, suhu berubah secara acak
            mean = 0  # Nilai rata-rata perubahan suhu (tidak ada perubahan)
            std_deviation = 0.2  # Deviasi standar, mengontrol seberapa besar fluktuasi suhu
            temperature_noise = np.random.normal(mean, std_deviation)
            self.current_condition["temperature"] += temperature_noise

        # Pastikan suhu tidak naik di atas 30°C atau turun di bawah 10°C
        self.current_condition["temperature"] = np.clip(self.current_condition["temperature"], 10, 30)

    # def control_ac(self):
    #     if 9 <= self.current_condition["time"][0] < 14:
    #         if self.current_condition["temperature"] < 30 and not self.ac_active:
    #             if self.current_condition["temperature"] >= 30:
    #                 self.ac_active = True  # Aktifkan AC saat suhu mencapai 30 derajat
    #         elif self.ac_active:
    #             self.current_condition["temperature"] -= 0.083
    #             if self.current_condition["temperature"] <= 20:
    #                 self.ac_active = False  # Matikan AC saat suhu mencapai 20 derajat
    #     elif 14 <= self.current_condition["time"][0] <= 18 and self.current_condition["temperature"] > 25:
    #         self.current_condition["temperature"] -= 0.083
    #         self.ac_active = False  # Pastikan AC mati di luar jam 9-14
    #     else:
    #         self.current_condition["temperature"] -= 0
    #         self.ac_active = False  # Pastikan AC mati di luar jam 9-14
    
    def control_ac(self):
        if 9 <= self.current_condition["time"][0] < 14:
            if not self.ac_active and self.current_condition["temperature"] >= 30:
                self.ac_active = True  # Aktifkan AC saat suhu mencapai 30 derajat
            if self.ac_active:
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
                self.simulate_temperature_with_noise()
                self.control_ac()
                self.control_lamp()
                if 6 <= hour < 18:
                    # Siang hari - suhu naik
                    self.current_condition["temperature"] += 0.02
                else:
                    # Malam hari - suhu turun
                    self.current_condition["temperature"] -= 0.02
                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                self.total_energy_consumption_day += total_energy_consumption / 60  # Menghitung total konsumsi per menit
                print(f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
                time.sleep(0.01)  # Simulate 1 minute delay

        # Konversi total konsumsi energi harian ke kWh
        total_energy_consumption_day_kwh = self.total_energy_consumption_day / 1000
        print(f"Total Energy Consumption for the Day: {total_energy_consumption_day_kwh:.2f} kWh")
