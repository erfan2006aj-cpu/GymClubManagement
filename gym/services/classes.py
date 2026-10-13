from gym.models import GymClass
class ClassService:
    def __init__(self):
        self.classes = []
    def add_class(self, gym_class):
        self.classes.append(gym_class)
    def get_all_classes(self):
        return self.classes