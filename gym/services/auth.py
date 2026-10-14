from gym.exceptions import (
    NotFoundError,
    ValidationError,
    AccountDisabledError,
)
from gym.services.users import get_user_by_username
from gym.models import Manager, Coach, Member
from gym.storage import Storage

DATA_PATH = "data/gym_data.txt"
USER_PREFIX = "USER"

def load_users() -> list:
    
    storage = Storage(DATA_PATH)
    
    if not storage.exists():
        return []
    
    users = []
    for line in storage.read_lines():
        line = line.strip()
        
        if not line or not line.startswith(USER_PREFIX + ","):
            continue
        
        try:
            parts = line.split(",")
            
            if len(parts) < 8:
                continue
            
            user_id = int(parts[1])
            name = parts[2]
            username = parts[3]
            password = parts[4]
            email = parts[5]
            role = parts[6]
            is_active = parts[7] == "True"
            
            if role == "manager":
                user = Manager(
                    id=user_id,
                    name=name,
                    username=username,
                    password=password,
                    email=email,
                    is_active=is_active,
                )
            elif role == "coach":
                user = Coach(
                    id=user_id,
                    name=name,
                    username=username,
                    password=password,
                    email=email,
                    is_active=is_active,
                )
            elif role == "member":
                user = Member(
                    id=user_id,
                    name=name,
                    username=username,
                    password=password,
                    email=email,
                    is_active=is_active,
                )
            else:
                continue
            
            users.append(user)
        
        except (ValueError, IndexError):
            
            continue
    
    return users


def save_users(users: list) -> None:
    
    storage = Storage(DATA_PATH)
    
    other_lines = []
    if storage.exists():
        for line in storage.read_lines():
            if line.strip() and not line.startswith(USER_PREFIX + ","):
                other_lines.append(line)
    
   
    user_lines = []
    for user in users:
        user_lines.append(
            f"{USER_PREFIX},{user.id},{user.name},{user.username},"
            f"{user.password},{user.email},{user.role},{user.is_active}"
        )
    
    storage.write_lines(other_lines + user_lines)


def login(username: str, password: str, role: str, users: list):
    
    if not username or not str(username).strip():
        raise ValidationError("نام کاربری نمی‌تواند خالی باشد.")
    
    if not password or not str(password).strip():
        raise ValidationError("رمز عبور نمی‌تواند خالی باشد.")
    
    username = str(username).strip()
    password = str(password).strip()
    role = str(role).strip().lower()
    
   
    user = get_user_by_username(username, users)
    
    if user is None:
        raise NotFoundError("نام کاربری یا رمز عبور اشتباه است.")
    
   
    if user.role != role:
        raise NotFoundError("نام کاربری یا رمز عبور اشتباه است.")
    
    
    if user.password != password:
        raise NotFoundError("نام کاربری یا رمز عبور اشتباه است.")
    
    
    if not user.is_active:
        raise AccountDisabledError("حساب کاربری شما غیرفعال است.")
    
   
    return user


def login_flow(role: str, users: list):
   
    
    role_names = {
        "manager": "مدیر باشگاه",
        "coach": "مربی",
        "member": "عضو باشگاه",
    }
    
    role_label = role_names.get(role, role)
    
    while True:
        print(f"\n{'=' * 45}")
        print(f"ورود {role_label}".center(45))
        print(f"{'=' * 45}")
        print("(برای بازگشت 0 وارد کنید)")
        print("-" * 45)
        
        username = input("نام کاربری: ").strip()
        if username == "0":
            return None
        
        password = input("رمز عبور: ").strip()
        if password == "0":
            return None
        
        try:
            user = login(username, password, role, users)
            print(f"\n✅ خوش آمدی {user.name}!")
            return user
        
        except ValidationError as e:
            print(f"\n❌ {e}")
        except NotFoundError as e:
            print(f"\n❌ {e}")
        except AccountDisabledError as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ خطای غیرمنتظره: {e}")
        
        
        print()
        choice = input("1. تلاش مجدد  2. بازگشت: ").strip()
        if choice == "2":
            return None