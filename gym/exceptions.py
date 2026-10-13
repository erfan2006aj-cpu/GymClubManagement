class GymError(Exception):
    pass
    #"پایه همه خطاهای برنامه"

class NotFoundError(GymError):
    pass
    #"موجودیت درخواستی در سیستم وجود نداره"
    
class ValidationError(GymError):
    pass
    #"داده یا ورودی  نامعتبر است"

class AccessDeniedError(GymError):
    pass
    #"کاربر اجازه انجام این عملیات رو نداره"

class DuplicateError(GymError):
    pass
    #"رکورد تکراری"

class AccountDisabledError(GymError):
    pass
    #"حساب غیرفعال است"

class InsufficientBalanceError(GymError):
    pass
    #"موجودی کیف پول کافی نیست"
