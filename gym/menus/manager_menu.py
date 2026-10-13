
from gym.services.users import (
    add_user,
    update_user,
    activate_user,
    deactivate_user,
    get_user_by_username,
    get_all_users,
)

def print_user(user):
    print("\n--------------------")
    print(f"Name: {user.name}")
    print(f"Username: {user.username}")
    print(f"Role: {user.role}")
    print(f"Email: {user.email}")
    print(f"Active: {user.is_active}")


def user_management_menu(users):
    while True:
        print("\n===== User Management =====")
        print("1. Add User")
        print("2. Find User")
        print("3. Update User")
        print("4. Activate User")
        print("5. Deactivate User")
        print("6. Show All Users")
        print("7. Back")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                role = input("Role (member/coach): ").strip()
                name = input("Name: ").strip()
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                email = input("Email: ").strip()
                status = input("Active? (y/n): ").strip().lower()

                if status not in ("y", "n"):
                    print("Please enter y or n.")
                    continue

                user = add_user(
                    name=name,
                    username=username,
                    password=password,
                    email=email,
                    role=role,
                    existing_users=users,
                    is_active=(status == "y"),
                )

                user.id = max(
                    (item.id or 0 for item in users), default=0
                ) + 1
                users.append(user)
                print("User added successfully.")

            elif choice == "2":
                username = input("Username: ").strip()
                user = get_user_by_username(username, users)

                if user is None:
                    print("User not found.")
                else:
                    print_user(user)

            elif choice == "3":
                username = input("Username to update: ").strip()
                user = get_user_by_username(username, users)

                if user is None:
                    print("User not found.")
                    continue

                print("Press Enter to keep the current value.")
                name = input(f"Name [{user.name}]: ")
                new_username = input(f"Username [{user.username}]: ")
                password = input("New password: ")
                email = input(f"Email [{user.email}]: ")

                update_user(
                    user,
                    name=name if name.strip() else None,
                    username=(
                        new_username if new_username.strip() else None
                    ),
                    password=password if password.strip() else None,
                    email=email if email.strip() else None,
                    existing_users=users,
                )
                print("User updated successfully.")

            elif choice == "4":
                username = input("Username to activate: ").strip()
                user = get_user_by_username(username, users)

                if user is None:
                    print("User not found.")
                else:
                    activate_user(user)
                    print("User activated successfully.")

            elif choice == "5":
                username = input("Username to deactivate: ").strip()
                user = get_user_by_username(username, users)

                if user is None:
                    print("User not found.")
                else:
                    deactivate_user(user)
                    print("User deactivated successfully.")

            elif choice == "6":
                all_users = get_all_users(users)

                if not all_users:
                    print("No users found.")
                else:
                    for user in all_users:
                        print_user(user)

            elif choice == "7":
                return

            else:
                print("Invalid choice. Please try again.")

        except ValueError as error:
            print(f"Error: {error}")


def manager_menu():
    users = []

    while True:
        print("\n===== Manager Menu =====")
        print("1. User Management")
        print("2. Hall Management")
        print("3. Class Management")
        print("4. Subscription and Payment Management")
        print("5. View Reports")
        print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user_management_menu(users)
        elif choice == "2":
            print("Hall Management selected")
        elif choice == "3":
            print("Class Management selected")
        elif choice == "4":
            print("Subscription and Payment Management selected")
        elif choice == "5":
            print("View Reports selected")
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
