from gym.services.users import UserService

def print_user(user):
    print("\n--------------------")
    print(f"ID: {user.id}")
    print(f"Name: {user.name}")
    print(f"Username: {user.username}")
    print(f"Role: {user.role}")
    print(f"Email: {user.email}")
    print(f"Active: {user.is_active}")


def user_management_menu(user_service):
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
                role = input("Role (member/coach): ").strip().lower()
                name = input("Name: ").strip()
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                email = input("Email: ").strip()
                status = input("Active? (y/n): ").strip().lower()

                if status not in ("y", "n"):
                    print("Please enter y or n.")
                    continue

                user = user_service.add(
                    name=name,
                    username=username,
                    password=password,
                    email=email,
                    role=role,
                )

                if status == "n":
                    user_service.set_active(user, False)

                print("User added successfully.")
                print_user(user)

            elif choice == "2":
                username = input("Username: ").strip()
                user = user_service.find_by_username(username)

                if user is None:
                    print("User not found.")
                else:
                    print_user(user)

            elif choice == "3":
                username = input("Username to update: ").strip()
                user = user_service.find_by_username(username)

                if user is None:
                    print("User not found.")
                    continue

                print("Press Enter to keep the current value.")
                name = input(f"Name [{user.name}]: ")
                new_username = input(f"Username [{user.username}]: ")
                password = input("New password: ")
                email = input(f"Email [{user.email}]: ")

                changes = {
                    "name": name if name.strip() else None,
                    "username": (
                        new_username if new_username.strip() else None
                    ),
                    "password": password if password.strip() else None,
                    "email": email if email.strip() else None,
                }

                changes = {
                    key: value
                    for key, value in changes.items()
                    if value is not None
                }

                user_service.update(user, **changes)
                print("User updated successfully.")
                print_user(user)

            elif choice == "4":
                username = input("Username to activate: ").strip()
                user = user_service.find_by_username(username)

                if user is None:
                    print("User not found.")
                else:
                    user_service.set_active(user, True)
                    print("User activated successfully.")

            elif choice == "5":
                username = input("Username to deactivate: ").strip()
                user = user_service.find_by_username(username)

                if user is None:
                    print("User not found.")
                else:
                    user_service.set_active(user, False)
                    print("User deactivated successfully.")

            elif choice == "6":
                all_users = user_service.list_all()

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
        except OSError as error:
            print(f"Could not save changes: {error}")

def manager_menu():
    user_service = UserService()

    while True:
        print("\n===== Manager Menu =====")
        print("1. User Management")
        print("2. Hall Management")
        print("3. Class Management")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user_management_menu(user_service)

        elif choice == "2":
            print("Hall Management selected.")

        elif choice == "3":  
            print("Class Management selected.")

        elif choice == "4":
            print("Logging out...")
            return

        else:
            print("Invalid choice. Please try again.")
