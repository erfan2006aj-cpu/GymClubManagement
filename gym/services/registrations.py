import random
from gym.models import Registration
class Registration_service:
    def __init__(self,registrations: list[Registration],class_service):
        self.registrations = registrations
        self.class_service = class_service
        self.next_id = max([r.id for r in registrations], default=0) + 1

    def generate_traking_number(self) -> int:
        while True:
            number = random.randint(100000, 999999)
            if not any(r.tracking_number == number for r in self.registrations):
                return number

    def find_active(self, member_id: int, class_id: int):
        for r in self.registrations:
            if (r.member_id == member_id and r.class_id == class_id and r.is_active):
                return r
        return None

    def is_registered(self, member_id: int, class_id: int) -> bool:
        return self.find_active(member_id, class_id) is not None

    def register(self,member,class_id: int,subscription_service,) -> Registration:
        pass

    def cancel_registration(self, member_id: int, class_id: int) -> Registration:
        pass

    def get_member_registrations(self, member_id: int) -> list[Registration]:
        pass

    def get_class_members(self, class_id: int) -> list[Registration]:
        pass
    