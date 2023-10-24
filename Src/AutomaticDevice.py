from ElectronicDevice import ElectronicDevice


class AutomaticDevice(ElectronicDevice):
    def __init__(self, name, energy_cost, control_condition, turn_off_condition):
        super().__init__(name, energy_cost)
        self.control_condition = control_condition  # Function to check when to turn on
        self.turn_off_condition = turn_off_condition  # Function to check when to turn off
        self.active = False

    def is_active(self, current_condition):
        if self.active and self.turn_off_condition(current_condition):
            self.turn_off()
        elif not self.active and self.control_condition(current_condition):
            self.turn_on()
        return self.active

    def turn_off(self):
        self.active = False
        print(f"{self.name} is turned off")

    def turn_on(self):
        self.active = True
        print(f"{self.name} is turned on")