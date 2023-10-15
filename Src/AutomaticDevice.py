from ElectronicDevice import ElectronicDevice

class AutomaticControlledDevice(ElectronicDevice):
    def __init__(self, name, energy_cost, control_condition):
        super().__init__(name, energy_cost)
        self.control_condition = control_condition  # Function to check when to turn on

    def is_active(self, current_condition):
        return self.control_condition(current_condition)
