from datetime import datetime, timedelta

class BoxManager:
    def __init__(self, box_name, initial_time = datetime.strptime("12:00:00", '%H:%M:%S')):
        self.box_name = box_name
        self.boxtime = initial_time

    def increment_boxtime(self):
        """Increment the box time by 15 minutes."""
        self.boxtime += timedelta(minutes=15)

    def decrement_boxtime(self):
        """Decrement the box time by 15 minutes."""
        self.boxtime -= timedelta(minutes=15)

    def get_boxtime(self):
        """Returns the current box time."""
        return self.boxtime.strftime('%H:%M')
