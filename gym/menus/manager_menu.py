def manager_menu():
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
            user_management_menu()
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
