# pip install pandas
import pandas as pd
import time
import numpy as np
import random

from AutomaticDevice import AutomaticDevice
     
class Smarthome:
    # df = pd.DataFrame(columns=['Time', 'Temperature', 'Energy Consumption', 'Total Energy Consumption (kWh)'])
    
    
    def __init__(self):
        self.rooms = []
        self.current_condition = {
            "temperature": 25,  # temperatur awal
            "time": (0, 0)      # 
        }
        self.ac_active = False  # Tambahkan atribut ini untuk melacak status AC
        self.lamp_active = False  # Tambahkan atribut ini untuk melacak status lampu
        self.total_energy_consumption_day = 0
        # self.total_energy_consumption_day=0
        # self.total_energy_consumption_day_kwh =0
        # self.total_energy_month=0
    def add_room(self, room):
        self.rooms.append(room)

    
    def control_ac(self):
        if 9 <= self.current_condition["time"][0] < 14:
            if self.current_condition["temperature"] < 30 and not self.ac_active:
                mean = 0  # Nilai rata-rata perubahan suhu (tidak ada perubahan)
                std_deviation = 1  # Deviasi standar, mengontrol seberapa besar fluktuasi suhu
                temperature_noise = np.random.normal(mean, std_deviation)
                self.current_condition["temperature"] += temperature_noise
                # Pastikan suhu tidak kurang dari 0°C
                if self.current_condition["temperature"] < 0:
                    self.current_condition["temperature"] = 0
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
       
    # def simulate_24_hours(self):
    #     # df = pd.DataFrame(columns=['Time', 'Temperature', 'Energy Consumption', 'Total Energy Consumption (kWh)'])
    #     data = []
    #     for hour in range(24):
    #         for minute in range(60):
    #             self.current_condition["time"] = (hour, minute)
    #             self.control_ac()
    #             self.control_lamp()
    #             total_energy_consumption = 0

    #             for room in self.rooms:
    #                 room.calculate_total_energy_consumption(self.current_condition)
    #                 total_energy_consumption += room.total_energy_consumption

    #             data.append({
    #                 "Time": f"{hour:02d}:{minute:02d}",
    #                 "Temperature": int(self.current_condition["temperature"]),
    #                 "Energy Consumption": total_energy_consumption,
    #             })

    #     df = pd.DataFrame(data)
    #     df.to_csv('daily_energy_consumption.csv', index=False)
    #     print("Daily simulation completed.")

        
        
        # for hour in range(24):
        #     for minute in range(60):
        #         self.current_condition["time"] = (hour, minute)
        #         self.control_ac()
        #         self.control_lamp()
        #         for room in self.rooms:
        #             room.calculate_total_energy_consumption(self.current_condition)
        #             data.append({
        #             "Hour": hour,
        #             "Room": room.name,
        #             "Total Energy Consumption": room.total_energy_consumption
        #         })
        #         total_energy_consumption = sum(room.total_energy_consumption for room in self.rooms)
                # self.total_energy_consumption_day += total_energy_consumption / 144  # Menghitung total konsumsi per menit
                # total_energy_consumption_day_kwh = self.total_energy_consumption_day / 1000

                # print(f"Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt")
                # time.sleep(0.01)  # Simulate 1 minute delay
                # output="Time: {hour:02d}:{minute:02d}, Temperature: {int(self.current_condition['temperature'])}°C, Total Energy Consumption: {total_energy_consumption} Watt"                

        # df = pd.DataFrame(data)
        # df.to_csv('dataset.data_ruangan.csv', index=False)  # index=False untuk tidak menyertakan indeks
        # df.to_csv('data_simulasi')
        # print(df)
        
    # def simulate_month(self):
    #     # month_data = []  # Menyimpan data total energi konsumsi per bulan
    #     # self.total_energy_month=0
    #     # for month in range(1, 31):
    #     #     self.simulate_24_hours()
    #     #     self.total_energy_month=self.total_energy_consumption_day/1000
    #     #     total_energy_formatted = round(self.total_energy_month, 2)
    #     #     month_data.append({
    #     #         "Day": "Day " + str(month),
    #     #         "Total Energy Consumption (kWh)": total_energy_formatted
    #     #     })
    #     # df = pd.DataFrame(month_data)
    #     # df.set_index("Day", inplace=True)
    #     # df.to_csv('total_energy_per_day.csv')
    #     # print("Simulation for a month completed.")
    #     month_data = []
    #     self.total_energy_month = 0

    #     for day in range(1, 31):
    #         self.simulate_24_hours()
    #         self.total_energy_month += self.total_energy_consumption_day
    #         total_energy_formatted = round(self.total_energy_month / 1000, 2)
    #         month_data.append({
    #             "Day": f"Day {day}",
    #             "Total Energy Consumption (kWh)": total_energy_formatted
    #         })

    #     df = pd.DataFrame(month_data)
    #     df.set_index("Day", inplace=True)
    #     df.to_csv('monthly_energy_consumption.csv')
    #     print("Monthly simulation completed.")

        
    def simulate_24_hours(self):
        data = []
        self.total_energy_consumption_day = 0  # Reset daily energy consumption

        for hour in range(24):
            for minute in range(60):
                self.current_condition["time"] = (hour, minute)
                self.control_ac()
                self.control_lamp()
                total_energy_consumption = 0

                for room in self.rooms:
                    room.calculate_total_energy_consumption(self.current_condition)
                    total_energy_consumption += room.total_energy_consumption

                self.total_energy_consumption_day += total_energy_consumption  # Accumulate daily energy consumption

                data.append({
                    "Time": f"{hour:02d}:{minute:02d}",
                    "Temperature": int(self.current_condition["temperature"]),
                    "Energy Consumption": total_energy_consumption,
                })

        df = pd.DataFrame(data)
        df.to_csv('daily_energy_consumption.csv', index=False)
        print("Daily simulation completed.")

    def simulate_month(self):
        month_data = []

        for day in range(1, 31):
            self.simulate_24_hours()

            total_energy_formatted = round(self.total_energy_consumption_day / 1000, 2)
            month_data.append({
                "Day": f"Day {day}",
                "Total Energy Consumption (kWh)": total_energy_formatted
            })

        df = pd.DataFrame(month_data)
        df.set_index("Day", inplace=True)
        df.to_csv('monthly_energy_consumption.csv')
        print("Monthly simulation completed.")