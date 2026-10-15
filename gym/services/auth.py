from gym.exceptions import (
    NotFoundError,
    ValidationError,
    AccountDisabledError,
)
from gym.services.users import UserService


def login(username: str, password: str, role: str, user_service: UserService):
    
    
    # 1. Validate inputs
    if not username or not str(username).strip():
        raise ValidationError("Username cannot be empty.")
    
    if not password or not str(password).strip():
        raise ValidationError("Password cannot be empty.")
    
    username = str(username).strip()
    password = str(password).strip()
    role = str(role).strip().lower()
    
    # 2. Find user
    user = user_service.find_by_username(username)
    
    if user is None:
        raise NotFoundError("Invalid username or password.")
    
    # 3. Check role
    if user.role != role:
        raise NotFoundError("Invalid username or password.")
    
    # 4. Check password
    if user.password != password:
        raise NotFoundError("Invalid username or password.")
    
    # 5. Check if account is active
    if not user.is_active:
        raise AccountDisabledError("Your account has been disabled.")
    
    # 6. Success
    return user


def login_flow(role: str, user_service: UserService):
    
    role_names = {
        "manager": "Manager",
        "coach": "Coach",
        "member": "Member",
    }
    
    role_label = role_names.get(role, role)
    
    while True:
        print(f"\n{'=' * 45}")
        print(f"{role_label} Login".center(45))
        print(f"{'=' * 45}")
        print("(Enter 0 to go back)")
        print("-" * 45)
        
        username = input("Username: ").strip()
        if username == "0":
            return None
        
        password = input("Password: ").strip()
        if password == "0":
            return None
        
        try:
            user = login(username, password, role, user_service)
            print(f"\n[OK] Welcome {user.name}!")
            return user
        
        except ValidationError as e:
            print(f"\n[ERROR] {e}")
        except NotFoundError as e:
            print(f"\n[ERROR] {e}")
        except AccountDisabledError as e:
            print(f"\n[ERROR] {e}")
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
        
        print()
        choice = input("1. Try again  2. Back: ").strip()
        if choice == "2":
            return None