class MemberMenu:
    def __init__(self, member, registration_service: Registration_service,class_service, subscription_service):
        self.member = member
        self.registration_service = registration_service
        self.class_service = class_service
        self.subscription_service = subscription_service

    def show(self):
        while True:
            print("\n Member Menu")
            print("1. Show availble classes")
            print("2. Register in class")
            print("3. Cancel registeration")
            print("4. My registerations")
            print("0. Exit")
            choice = input("Enter a number : ")

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
        pass

    def register_to_class(self):
        pass

    def cancel_registration(self):
        pass

    def show_my_registrations(self):
        pass
