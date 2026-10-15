import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from gym.services.users import UserService
from gym.services.auth import login_flow
from gym.exceptions import GymError


def print_header(title: str) -> None:
    print("\n" + "=" * 45)
    print(title.center(45))
    print("=" * 45)


def show_main_menu() -> None:
    print_header("Gym Club Management System")
    print("1. Manager Login")
    print("2. Coach Login")
    print("3. Member Login")
    print("4. Exit")
    print("-" * 45)


def handle_manager_login(user_service: UserService) -> None:
    user = login_flow("manager", user_service)
    if user is None:
        return
    
    try:
        from gym.menus.manager_menu import manager_menu
        manager_menu(user_service)   
    except Exception as e:
        print(f"\n[ERROR] Manager panel error: {e}")


def handle_coach_login(user_service: UserService) -> None:
    user = login_flow("coach", user_service)
    if user is None:
        return
    try:
        from gym.services.classes import ClassService
        from gym.services.registrations import Registration_service
        from gym.services.workout import WorkoutService
        from gym.menus.trainer_menu import trainer_menu

        
        class_service = ClassService()
        registration_service = Registration_service([], class_service)
        workout_service = WorkoutService(class_service, registration_service)

        
        trainer_menu(
            coach_id=user.id,
            workout_service=workout_service,
            class_service=class_service,
            registration_service=registration_service,
        )
    except Exception as e:
        print(f"\n[ERROR] Coach panel error: {e}")

def handle_member_login(user_service: UserService) -> None:
    user = login_flow("member", user_service)
    if user is None:
        return

    try:
        from gym.services.classes import ClassService
        from gym.services.registrations import Registration_service
        from gym.services.subscriptions import SubscriptionService
        from gym.services.wallet import WalletService
        from gym.menus.member_menu import MemberMenu

        # Build services
        class_service = ClassService()
        registration_service = Registration_service([], class_service)
        subscription_service = SubscriptionService()
        wallet_service = WalletService(user_service, subscription_service)

        # Build member menu
        member_menu = MemberMenu(
            member=user,
            registration_service=registration_service,
            class_service=class_service,
            subscription_service=subscription_service,
        )

        # Show menu
        member_menu.show()
    except Exception as e:
        print(f"\n[ERROR] Member panel error: {e}")


def main() -> None:
    print("\nLoading data...")
    try:
        user_service = UserService()
        print(f"[OK] {len(user_service.users)} user(s) loaded.")
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return
    
    while True:
        try:
            show_main_menu()
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                handle_manager_login(user_service)
            
            elif choice == "2":
                handle_coach_login(user_service)
            
            elif choice == "3":
                handle_member_login(user_service)
            
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
