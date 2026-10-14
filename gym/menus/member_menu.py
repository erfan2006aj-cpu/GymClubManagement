class MemberMenu:
    def __init__(self, member, registration_service: Registration_service,
                 class_service, subscription_service):
        self.member = member
        self.registration_service = registration_service
        self.class_service = class_service
        self.subscription_service = subscription_service