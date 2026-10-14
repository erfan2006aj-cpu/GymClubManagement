class MemberMenu:
    def __init__(self, member, registration_service: Registration_service,class_service, subscription_service):
        self.member = member
        self.registration_service = registration_service
        self.class_service = class_service
        self.subscription_service = subscription_service

    def show(self):
        while True:
            print("\n ====Member Menu====")
            print("1. Show availble classes")
            print("2. Register in class")
            print("3. Cancel registeration")
            print("4. My registerations")
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
        pass

    def cancel_registration(self):
        pass

    def show_my_registrations(self):
        pass
