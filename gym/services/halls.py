from gym.models import Hall
from gym.storage import Storage
class HallService:
    def __init__(self):
        self.storage = Storage("data/gym_data.txt")
        
    def add_hall(self, hall):
        all_halls = self.get_all_halls()
        for existing_hall in all_halls:
            if str(existing_hall.id) == str(hall.id):
                print("This hall ID already exists.")
                return
        data = (f"HALL,{hall.id},{hall.name},"
                f"{hall.capacity},{hall.is_active}")
        self.storage.append_line(data)
        print("Hall added successfully.")
    def get_all_halls(self):
        lines = self.storage.read_lines()
        data = "\n".join(lines)
        halls = []
        for line in data.splitlines():
            parts = line.split(",")
            if parts[0] == "HALL":
                hall = Hall(
                    id=parts[1],
                    name=parts[2],
                    capacity=int(parts[3]),
                    is_active=bool(parts[4] == "True"))
                halls.append(hall)
        return halls
