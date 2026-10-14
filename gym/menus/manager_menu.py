from gym.services.halls import HallService
from gym.services.classes import ClassService
from gym.models import Hall, GymClass



def manager_menu():
    hall_service = HallService()
    class_service = ClassService()
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
            print("\n===== Hall Management =====")
            print("1. Add Hall")
            print("2. View Halls")
            print("3. Back")

            hall_choice = input("Choose an option: ").strip()

            if hall_choice == "1":
                hall_id = input("Hall ID: ").strip()
                name = input("Hall name: ").strip()

                try:
                    capacity = int(input("Hall capacity: "))

                    hall = Hall(
                        id=hall_id,
                        name=name,
                        capacity=capacity,
                        is_active=True
                    )

                    hall_service.add_hall(hall)

                except ValueError:
                    print("Capacity must be a number.")

            elif hall_choice == "2":
                halls = hall_service.get_all_halls()

                if not halls:
                    print("No halls found.")
                else:
                    for hall in halls:
                        print(hall)

            elif hall_choice == "3":
                continue

            else:
                print("Invalid option.")
        elif choice == "3":
            print("\n===== Class Management =====")
            print("1. Add Class")
            print("2. View Classes")
            print("3. Back")

            class_choice = input("Choose an option: ").strip()

            if class_choice == "1":
                class_id = input("Class ID: ").strip()
                name = input("Class name: ").strip()
                coach_id = input("Coach ID: ").strip()
                hall_id = input("Hall ID: ").strip()

                try:
                    capacity = int(input("Class capacity: "))
                    schedule = input("Class schedule: ").strip()

                    halls = hall_service.get_all_halls()
                    hall_exists = False

                    for hall in halls:
                        if str(hall.id) == hall_id:
                            hall_exists = True
                            break

                    if not hall_exists:
                        print("Hall not found.")
                        continue

                    gym_class = GymClass(
                        id=class_id,
                        name=name,
                        coach_id=coach_id,
                        hall_id=hall_id,
                        capacity=capacity,
                        schedule=schedule,
                        is_active=True
                    )

                    class_service.add_class(gym_class)

                except ValueError:
                    print("Capacity must be a number.")

            elif class_choice == "2":
                classes = class_service.get_all_classes()

                if not classes:
                    print("No classes found.")
                else:
                    for gym_class in classes:
                        print(gym_class)

            elif class_choice == "3":
                continue

            else:
                print("Invalid option.")

        elif choice == "4":
            print("Subscription and Payment Management selected")

        elif choice == "5":
            print("View Reports selected")

        elif choice == "6":
            print("Logging out...")
            break
