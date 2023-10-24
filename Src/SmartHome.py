import numpy as np
import pandas as pd
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
        self.daily_temperature_high = []  # List untuk menyimpan suhu maksimum harian
        self.daily_temperature_low = []  # List untuk menyimpan suhu minimum harian

    def add_room(self, room):
        self.rooms.append(room)

    def simulate_temperature_with_noise(self):
            # Simulasi pengaruh lingkungan
        if self.ac_active:
            pass
        else:
            
            # Pengaruh alami, misalnya, suhu berubah secara acak
            mean = 0  # Nilai rata-rata perubahan suhu (tidak ada perubahan)
            std_deviation = 0.2  # Deviasi standar, mengontrol seberapa besar fluktuasi suhu
            temperature_noise = np.random.normal(mean, std_deviation)
            self.current_condition["temperature"] += temperature_noise

        # Pastikan suhu tidak naik di atas 30°C atau turun di bawah 10°C
        self.current_condition["temperature"] = np.clip(self.current_condition["temperature"], 18, 32)
    
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
        data = []  # Membuat list kosong untuk menyimpan data simulasi
        self.total_energy_consumption_day = 0
        for hour in range(24):
            for minute in range(60):
                self.current_condition["time"] = (hour, minute)
                self.simulate_temperature_with_noise()
                self.control_ac()
                self.control_lamp()
                if 6 <= hour < 15:
                    # Siang hari - suhu naik
                    self.current_condition["temperature"] += 0.02
                elif 20 <= hour <= 23:
                    # Malam hari - suhu turun
                    self.current_condition["temperature"] -= 0.02
                else:
                    pass
                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                self.total_energy_consumption_day += total_energy_consumption / 60  # Menghitung total konsumsi per menit

                # Simpan suhu maksimum dan minimum harian
                if minute == 0:
                    self.daily_temperature_high.append(self.current_condition["temperature"])
                    self.daily_temperature_low.append(self.current_condition["temperature"])

                # Update suhu maksimum dan minimum harian
                if self.current_condition["temperature"] > self.daily_temperature_high[-1]:
                    self.daily_temperature_high[-1] = self.current_condition["temperature"]
                elif self.current_condition["temperature"] < self.daily_temperature_low[-1]:
                    self.daily_temperature_low[-1] = self.current_condition["temperature"]

                print(f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
                time.sleep(0.01)  # Simulate 1 minute delay

        # Konversi total konsumsi energi harian ke kWh
        total_energy_consumption_day_kwh = self.total_energy_consumption_day / 1000
        print(total_energy_consumption_day_kwh)

        # Dapatkan tanggal saat ini
        current_date = pd.Timestamp.now().date()

        # Buat DataFrame dengan satu baris data
        data = pd.DataFrame({'Date': [current_date], 'Energy Consumption (kWh)': [total_energy_consumption_day_kwh],
                             'Temperature High (°C)': [max(self.daily_temperature_high)],
                             'Temperature Low (°C)': [min(self.daily_temperature_low)]})

        try:
            existing_data = pd.read_csv("daily_energy_consumption.csv")
            updated_data = pd.concat([existing_data, data], ignore_index=True)
            updated_data.to_csv("daily_energy_consumption.csv", index=False, float_format='%.3f')
        except FileNotFoundError:
            data.to_csv("daily_energy_consumption.csv", index=False, float_format='%.3f')