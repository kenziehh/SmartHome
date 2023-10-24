import random

import numpy as np
import time

from matplotlib import pyplot as plt

from AutomaticDevice import AutomaticDevice

class Smarthome:
    def __init__(self):
        self.energy_consumption_data = []
        self.temperature_data = []
        self.rooms = []
        self.current_condition = {
            "temperature": 22,  # Initial temperature
            "time": (0, 0)  # Initial time (hour, minute)
        }

        self.total_energy_consumption_day = 0
        self.daily_temperature_high = []  # List untuk menyimpan suhu maksimum harian
        self.daily_temperature_low = []  # List untuk menyimpan suhu minimum harian

    def add_room(self, room):
        self.rooms.append(room)

    def simulate_temperature_with_noise(self, hour, max_temp, min_temp):
        # Simulasi pengaruh lingkungan
        if 6 <= hour < 11:
            # Siang hari - suhu naik
            self.current_condition["temperature"] += 0.03
        elif 13 <= hour <= 23:
            # Malam hari - suhu turun
            self.current_condition["temperature"] -= 0.014

        # Pengaruh alami, misalnya, suhu berubah secara acak
        mean = 0  # Nilai rata-rata perubahan suhu (tidak ada perubahan)
        std_deviation = 0.05  # Deviasi standar, mengontrol seberapa besar fluktuasi suhu
        temperature_noise = np.random.normal(mean, std_deviation)
        self.current_condition["temperature"] += temperature_noise

        # Pastikan suhu tidak naik di atas max_temp atau turun di bawah min_temp
        self.current_condition["temperature"] = np.clip(self.current_condition["temperature"], min_temp, max_temp)

    def control_ac(self):
        hour = self.current_condition["time"][0]

        for room in self.rooms:
            for device in room.devices.items():
                if isinstance(device, AutomaticDevice) and device.name == "Air Conditioner":
                   print("HELLO AC")
                else:
                    print("tak de ac")

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
        data = []  # Membuat list kosong untuk menyimpan data simulasi
        self.total_energy_consumption_day = 0
        max_temp = random.uniform(30, 36)
        min_temp = random.uniform(18, 22)

        for hour in range(24):
            for minute in range(60):
                self.current_condition["time"] = (hour, minute)
                self.simulate_temperature_with_noise(hour, max_temp, min_temp)
                self.control_ac()
                self.control_lamp()

                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                self.total_energy_consumption_day += total_energy_consumption / 60  # Menghitung total konsumsi per menit

                # Simpan suhu maksimum dan minimum harian
                if minute == 0:
                    self.daily_temperature_high.append(self.current_condition["temperature"])
                    self.daily_temperature_low.append(self.current_condition["temperature"])

                # # Update suhu maksimum dan minimum harian
                # if self.current_condition["temperature"] > self.daily_temperature_high[-1]:
                #     self.daily_temperature_high[-1] = self.current_condition["temperature"]
                # elif self.current_condition["temperature"] < self.daily_temperature_low[-1]:
                #     self.daily_temperature_low[-1] = self.current_condition["temperature"]

                print(
                    f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
                self.temperature_data.append(self.current_condition['temperature'])
                self.energy_consumption_data.append(total_energy_consumption)
                time.sleep(0.000)  # Simulate 1 minute delay

        # Konversi total konsumsi energi harian ke kWh
        total_energy_consumption_day_kwh = self.total_energy_consumption_day / 1000
        print(f"KWh: {total_energy_consumption_day_kwh}")

        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)  # 2 rows, 1 column, first plot
        plt.plot(range(24 * 60), self.temperature_data, label='Temperature (°C)', color='blue')
        plt.title('Temperature Simulation Data')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.legend()

        # Plot Energy Consumption Data
        plt.subplot(2, 1, 2)  # 2 rows, 1 column, second plot
        plt.plot(range(24 * 60), self.energy_consumption_data, label='Energy Consumption (Watt)', color='red')
        plt.title('Energy Consumption Simulation Data')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Energy Consumption (Watt)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()  # Ensure subplots don't overlap
        plt.show()