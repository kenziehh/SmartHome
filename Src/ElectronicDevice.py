class ElectronicDevice:
    def __init__(self, name, energy_cost):
        self.name = name
        self.energy_cost = energy_cost  # Watt

    def get_total_energy_consumption(self, quantity):
        return self.energy_cost * quantity