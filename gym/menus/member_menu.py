from gym.services.registration_service import Registration_service
class MemberMenu:
    def __init__(self, member, registration_service: Registration_service,class_service, subscription_service):
        self.member = member
        self.registration_service = registration_service
        self.class_service = class_service
        self.subscription_service = subscription_service

    def show(self):
        while True:
            print("\n ====Member Menu====")
            print("1. Show available classes")
            print("2. Register in class")
            print("3. Cancel registration")
            print("4. My registrations")
            print("0. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.list_available_classes()
            elif choice == "2":
                self.register_to_class()
            elif choice == "3":
                self.cancel_registration()
            elif choice == "4":
                self.show_my_registrations()
            elif choice == "0":
                break
            else:
                print(f"'{choice}' is not a valid option. Please choose 0-4.")

    def list_available_classes(self):
        classes = self.class_service.get_all_classes()
        for c in classes:
            if not c.is_active:
                continue
            registered = len(self.registration_service.get_class_members(c.id))
            if registered >= c.capacity:
                continue
            remaining = c.capacity - registered
            print(f"ID= {c.id} | {c.name} |capacity: {remaining}")

    def register_to_class(self):
        try:
            class_id = int(input("Class Id :"))
            reg = self.registration_service.register(self.member, class_id, self.subscription_service)
            print(f"Registration was successful | tracking number : {reg.tracking_number}")
        except ValueError as e:
            print(f"Error : {e}")

    def cancel_registration(self):
        try:
            class_id = int(input("Class Id :"))
            reg = self.registration_service.cancel_registration(self.member.id, class_id)
            print(f"Cancellation was successful | tracking number : {reg.tracking_number}")
        except ValueError as e:
            print(f"Error : {e}")

    def show_my_registrations(self):
        regs = self.registration_service.get_member_registrations(self.member.id)
        if not regs:
            print("You do not have any active registration")
            return
        for r in regs:
            print(f"Class Id : {r.class_id} | Tracking number : {r.tracking_number} "
                  f"| Date : {r.registration_date:%Y-%m-%d %H:%M}")
