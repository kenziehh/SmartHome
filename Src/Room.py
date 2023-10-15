from AutomaticDevice import AutomaticControlledDevice


class Room:
    def __init__(self, name):
        self.name = name
        self.devices = {}  # Menggunakan kamus untuk menyimpan perangkat dan kuantitasnya
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
