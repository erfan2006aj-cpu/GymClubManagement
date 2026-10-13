from gym.models import Hall
class HallService:
    def __init__(self):
        self.halls = []
    def add_hall(self, hall):
        self.halls.append(hall)
    def get_all_halls(self):
        return self.halls