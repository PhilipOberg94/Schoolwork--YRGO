from datetime import datetime, timedelta

class BoxManager:
    def __init__(self, box_name, initial_time=datetime.strptime("12:00:00", '%H:%M:%S')):
        self.box_name = box_name
        self.boxtime = initial_time

    def increment_boxtime(self):
        self.boxtime += timedelta(minutes=15)

    def decrement_boxtime(self):
        self.boxtime -= timedelta(minutes=15)

    def get_boxtime(self):
        return self.boxtime.strftime('%H:%M')