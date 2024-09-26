class BoxManager:
    def __init__(self):
        self.box_times = {
            1: (6, 30),  # Box 1 opens at 06:30
            2: (7, 45),  # Box 2 opens at 07:45
        }

    def set_box_time(self, box_number, hour, minute):
        self.box_times[box_number] = (hour, minute)
        print(f"Box {box_number} set to open at {hour:02}:{minute:02}")

    def get_box_time(self, box_number):
        return self.box_times[box_number]
