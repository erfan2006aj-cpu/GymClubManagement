class GymError(Exception):
    pass

class NotFoundError(GymError):
    pass

class ValidationError(GymError):
    pass

class PermissionError(GymError):
    pass