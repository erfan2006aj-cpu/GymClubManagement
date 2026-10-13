from gym.models import GymClass
from gym.storage import Storage

class ClassService:
    def __init__(self):
        self.storage = Storage("data/gym_data.txt")
        
    def add_class(self, gym_class):
        all_classes = self.get_all_classes()
        for existing_class in all_classes:
            if str(existing_class.id) == str(gym_class.id):
                print("This class ID already exists.")
                return
        data = (
            f"CLASS,{gym_class.id},{gym_class.name},"
            f"{gym_class.coach_id},{gym_class.hall_id},"
            f"{gym_class.capacity},{gym_class.schedule},"
            f"{gym_class.is_active}"
        )
        self.storage.append_line(data)
        print("Class added successfully.")
        
    def get_all_classes(self):
        lines = self.storage.read_lines()
        data = "\n".join(lines)
        classes = []
        for line in data.splitlines():
            parts = line.split(",")
            if parts[0] == "CLASS":
                if len(parts) == 7:
                    schedule = "Not specified"
                    is_active = parts[6] == "True"
                else:
                    schedule = parts[6]
                    is_active = parts[7] == "True"

                gym_class = GymClass(
                    id=parts[1],
                    name=parts[2],
                    coach_id=parts[3],
                    hall_id=parts[4],
                    capacity=int(parts[5]),
                    schedule=schedule,
                    is_active=is_active
                )
                classes.append(gym_class)
        return classes
