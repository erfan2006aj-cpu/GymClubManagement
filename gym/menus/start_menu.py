from gym.menus.manager_menu import manager_menu


def start_menu():
    while True:
        print("\n===== Gym Club Management =====")
        print("1. Manager Login")
        print("2. Trainer Login")
        print("3. Member Login")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            manager_menu()

        elif choice == "2":
            print("Trainer login is not available yet.")

        elif choice == "3":
            print("Member login is not available yet.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")