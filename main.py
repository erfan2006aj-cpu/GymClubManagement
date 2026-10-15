"""
GymClub Management System
Main entry point
"""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from gym.services.auth import load_users, save_users, login_flow
from gym.models import Manager
from gym.storage import Storage
from gym.exceptions import GymError



DATA_PATH = "data/gym_data.txt"

DEFAULT_ADMIN = {
    "id": 1,
    "name": "Admin",
    "username": "admin",
    "password": "admin@123",
    "email": "admin@gym.com",
    "is_active": True,
}



def init_data() -> None:
    
    storage = Storage(DATA_PATH)
    
   
    if storage.exists():
        lines = storage.read_lines()
       
        if any(line.strip().startswith("USER,") for line in lines):
            return
    
   
    print("[INFO] First run detected. Creating default admin...")
    
    admin = Manager(
        id=DEFAULT_ADMIN["id"],
        name=DEFAULT_ADMIN["name"],
        username=DEFAULT_ADMIN["username"],
        password=DEFAULT_ADMIN["password"],
        email=DEFAULT_ADMIN["email"],
        is_active=DEFAULT_ADMIN["is_active"],
    )
    
    save_users([admin])
    
    print("=" * 45)
    print("  Default admin created:")
    print(f"    Username: {DEFAULT_ADMIN['username']}")
    print(f"    Password: {DEFAULT_ADMIN['password']}")
    print("  Please change the password after first login.")
    print("=" * 45)




def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 45)
    print(title.center(45))
    print("=" * 45)


def show_main_menu() -> None:
    """Display the start menu."""
    print_header("Gym Club Management System")
    print("1. Manager Login")
    print("2. Coach Login")
    print("3. Member Login")
    print("4. Exit")
    print("-" * 45)



def handle_manager_login(users: list) -> None:
    """Handle manager login and panel."""
    user = login_flow("manager", users)
    if user is None:
        return
    
    try:
        from gym.menus.manager_menu import manager_menu
        manager_menu(users)   
    except Exception as e:
        print(f"\n[ERROR] Manager panel error: {e}")


def handle_coach_login(users: list) -> None:
    """Handle coach login and panel."""
    user = login_flow("coach", users)
    if user is None:
        return
    
    try:
        from gym.services.classes import ClassService
        from gym.services.registrations import Registration_service
        from gym.menus.trainer_menu import trainer_menu
        
        class_service = ClassService()
        registration_service = Registration_service([], class_service)
        
        
        print("\n[INFO] Coach panel is under development.")
        
    except Exception as e:
        print(f"\n[ERROR] Coach panel error: {e}")


def handle_member_login(users: list) -> None:
    """Handle member login and panel."""
    user = login_flow("member", users)
    if user is None:
        return
    
    try:
        
        print("\n[INFO] Member panel is under development.")
        
    except Exception as e:
        print(f"\n[ERROR] Member panel error: {e}")



def main() -> None:
    
    init_data()
    
    
    print("\nLoading data...")
    try:
        users = load_users()
        print(f"[OK] {len(users)} user(s) loaded.")
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        users = []
    
    
    while True:
        try:
            show_main_menu()
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                handle_manager_login(users)
                
                users = load_users()
            
            elif choice == "2":
                handle_coach_login(users)
            
            elif choice == "3":
                handle_member_login(users)
            
            elif choice == "4":
                print("\nGoodbye!")
                break
            
            else:
                print("\n[ERROR] Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n[INFO] Program interrupted by user.")
            break
        except GymError as e:
            print(f"\n[ERROR] {e}")
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    main()
