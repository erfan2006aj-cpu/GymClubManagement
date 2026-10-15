from datetime import datetime
import random
from gym.models import Registration
from gym.storage import Storage
DATA_PATH = "data/gym_data.txt"
class Registration_service:
    def __init__(self, class_service):
        self.storage = Storage(DATA_PATH)
        self.registrations = self._load_registrations()
        self.class_service = class_service
        self.next_id = max((r.id for r in registrations), default=0) + 1

    def generate_tracking_number(self) -> int:
        used = {r.tracking_number for r in self.registrations}
        while True:
            number = random.randint(100000, 999999)
            if number not in used:
                return number

    def find_active(self, member_id: int, class_id: int):
        for r in self.registrations:
            if (r.member_id == member_id and r.class_id == class_id and r.is_active):
                return r
        return None

    def is_registered(self, member_id: int, class_id: int) -> bool:
        return self.find_active(member_id, class_id) is not None

    def register(self,member,class_id: int,subscription_service) -> Registration:

        gym_class = self.class_service.find_by_id(class_id)
        if gym_class is None:
            raise ValueError(f"Class with {class_id} class id does not exist")

        if not gym_class.is_active:                      
            raise ValueError("This class is not active")

        if self.is_registered(member.id, class_id):
            raise ValueError("You are already registered")

        if len(self.get_class_members(class_id)) >= gym_class.capacity:
            raise ValueError("The class is full")

        if not subscription_service.has_active_subscription(member.id):
            raise ValueError("You do not have subscription")

        registration = Registration(
            id=self.next_id,
            member_id=member.id,
            class_id=class_id,
            tracking_number=self.generate_tracking_number(),
            registration_date=datetime.now(),
            is_active=True
        )
        self.registrations.append(registration)
        self.next_id += 1
        return registration

    def cancel_registration(self, member_id: int, class_id: int) -> Registration:
        registration = self.find_active(member_id, class_id)
        if registration is None:
            raise ValueError("No active registration found")
        registration.cancel()
        self._rewrite_all()
        return registration

    def get_member_registrations(self, member_id: int) -> list[Registration]:
        return [r for r in self.registrations if r.member_id == member_id and r.is_active]

    def get_class_members(self, class_id: int) -> list[Registration]:
        return [r for r in self.registrations if r.class_id == class_id and r.is_active]

    def _load_registrations(self) -> list[Registration]:
        registrations = []
        for line in self.storage.read_lines():
            parts = line.split(",")
            if parts[0] == "REGISTRATION" and len(parts) == 7:
                registrations.append(Registration(
                    id=int(parts[1]),
                    class_id=int(parts[2]),
                    member_id=int(parts[3]),
                    tracking_number=parts[4],
                    is_active=parts[5] == "True",
                    registration_date=datetime.fromisoformat(parts[6]),
                ))
        return registrations

    def _save_registration(self, r: Registration):
        line = (
            f"REGISTRATION,{r.id},{r.class_id},{r.member_id},"
            f"{r.tracking_number},{r.is_active},"
            f"{r.registration_date.isoformat()}"
        )
        self.storage.append_line(line)

    def _rewrite_all(self):
        lines = []
        for r in self.registrations:
            lines.append(
                f"REGISTRATION,{r.id},{r.class_id},{r.member_id},"
                f"{r.tracking_number},{r.is_active},"
                f"{r.registration_date.isoformat()}"
            )
        self.storage.write_lines(lines)
