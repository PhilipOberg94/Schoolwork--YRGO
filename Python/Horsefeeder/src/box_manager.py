class BoxManager:
    def __init__(self):
        self.box_times = {i: (0, 0) for i in range(1, 9)}  # Initialize times for 8 boxes

    def set_box_time(self, box_number, hour, minute):
        self.box_times[box_number] = (hour, minute)

    def get_box_time(self, box_number):
        return self.box_times[box_number]
