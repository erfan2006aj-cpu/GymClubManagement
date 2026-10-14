class MemberMenu:
    def __init__(self, member, registration_service: Registration_service,class_service, subscription_service):
        self.member = member
        self.registration_service = registration_service
        self.class_service = class_service
        self.subscription_service = subscription_service

    def show(self):
        pass

    def list_available_classes(self):
        pass

    def register_to_class(self):
        pass

    def cancel_registration(self):
        pass

    def show_my_registrations(self):
        pass
