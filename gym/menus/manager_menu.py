from gym.services.users import UserService
from gym.services.halls import HallService
from gym.services.classes import ClassService
from gym.models import Hall, GymClass

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

def hall_management_menu(hall_service):
    
    while True:
        print("\n==== Hall Management ====")
        print("1. Add Hall")
        print("2. View All Halls")
        print("3. Back")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            try:
                name = input("Hall name: ").strip()
                capacity = input("Capacity: ").strip()
                equipment = input("Equipment (comma-separated): ").strip()
                
                from gym.models import Hall
                hall = Hall(
                    id="0",
                    name=name,
                    capacity=int(capacity),
                    equipment=equipment.split(",") if equipment else [],
                    is_active=True,
                )
                hall_service.add_hall(hall)
                
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            try:
                halls = hall_service.get_all_halls()
                if not halls:
                    print("No halls found.")
                else:
                    print(f"\n{'ID':<5} {'Name':<20} {'Capacity':<10} {'Active'}  ")
                    print("-" * 50)
                    for h in halls:
                        equipment_str = ", ".join(h.equipment) if h.equipment else "None"
                        print(f"{h.id:<5} {h.name:<20} {h.capacity:<10} {h.is_active}  {equipment_str}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")


def class_management_menu(class_service, user_service, hall_service):
    
    while True:
        print("\n==== Class Management ====")
        print("1. Add Class")
        print("2. View All Classes")
        print("3. Back")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            try:
                name = input("Class name: ").strip()
                if not name:
                    print("Error: Class name cannot be empty.")
                    continue
                
                coach_id = input("Coach ID: ").strip()
                if not coach_id:
                    print("Error: Coach ID cannot be empty.")
                    continue
                
                
                coach = user_service.find_by_id(coach_id)
                if coach is None:
                    print(f"Error: No user found with ID {coach_id}.")
                    continue
                
                
                if coach.role != "coach":
                    print(f"Error: User {coach.name} is not a coach (role: {coach.role}).")
                    continue
                
                
                if not coach.is_active:
                    print(f"Error: Coach {coach.name} is not active.")
                    continue
                
                hall_id = input("Hall ID: ").strip()
                if not hall_id:
                    print("Error: Hall ID cannot be empty.")
                    continue
                
                
                hall = hall_service.find_by_id(hall_id)
                if hall is None:
                    print(f"Error: No hall found with ID {hall_id}.")
                    continue
                
                
                if not hall.is_active:
                    print(f"Error: Hall {hall.name} is not active.")
                    continue
                
                capacity_str = input("Capacity: ").strip()
                if not capacity_str.isdigit() or int(capacity_str) <= 0:
                    print("Error: Capacity must be a positive integer.")
                    continue
                
                
                if int(capacity_str) > hall.capacity:
                    print(f"Error: Class capacity ({capacity_str}) exceeds hall capacity ({hall.capacity}).")
                    continue
                
                schedule = input("Schedule (for example: Saturday 10-12): ").strip()
                if not schedule:
                    print("Error: Schedule cannot be empty.")
                    continue
                
                
                
                from gym.models import GymClass
                gym_class = GymClass(
                    id="0",
                    name=name,
                    coach_id=str(coach.id),
                    hall_id=str(hall.id),
                    capacity=int(capacity_str),
                    schedule=schedule,
                    is_active=True,
                )
                
                class_service.add_class(gym_class)
            
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            try:
                classes = class_service.get_all_classes()
                if not classes:
                    print("No classes found.")
                else:
                    print(f"\n{'ID':<5} {'Name':<20} {'Coach':<8} {'Hall':<6} {'Cap':<5} {'Schedule':<20} {'Active'}")
                    print("-" * 80)
                    for c in classes:
                        print(f"{c.id:<5} {c.name:<20} {c.coach_id:<8} {c.hall_id:<6} {c.capacity:<5} {c.schedule:<20} {c.is_active}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            return
        
        else:
            print("Invalid choice. Please try again.")

def subscription_management_menu(subscription_service, user_service):
    while True:
        print("\n==== Subscription & Payments ====")
        print("1. Create Subscription for Member")
        print("2. View All Subscriptions")
        print("3. View Member Subscription Status")
        print("4. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                member_id = input("Member ID: ").strip()
                member = user_service.find_by_id(member_id)
                if member is None:
                    print(f"Error: No user found with ID {member_id}.")
                    continue

                print("\nAvailable plans:")
                for kind, plan in subscription_service.list_plans():
                    print(f"  {kind}: {plan['name']} - {plan['cost']}")

                kind = input("Choose plan: ").strip()
                price = subscription_service.get_plan_price(kind)
                sub = subscription_service.create_subscription(
                    member_id=member.id, kind=kind, amount=price,
                )
                print(f"OK! Tracking: {sub.tracking_number}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            subs = subscription_service.list_all()
            if not subs:
                print("No subscriptions found.")
            else:
                for s in subs:
                    print(f"ID={s.id} | Member={s.member_id} | Type={s.subscription_type} | Amount={s.amount} | Tracking={s.tracking_number}")

        elif choice == "3":
            try:
                member_id = input("Member ID: ").strip()
                member = user_service.find_by_id(member_id)
                if member is None:
                    print(f"Error: No user found with ID {member_id}.")
                    continue
                status = subscription_service.get_member_status(member.id)
                print(f"Subscription status: {status}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            return
        else:
            print("Invalid choice.")


def reports_menu(subscription_service, user_service, class_service):
    while True:
        print("\n==== Reports ====")
        print("1. Active Members")
        print("2. Active Coaches")
        print("3. Active Classes")
        print("4. Total Income")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                users = user_service.list_all()
                count = sum(1 for u in users if u.role == "member" and u.is_active)
                print(f"Active members: {count}")
            elif choice == "2":
                users = user_service.list_all()
                count = sum(1 for u in users if u.role == "coach" and u.is_active)
                print(f"Active coaches: {count}")
            elif choice == "3":
                classes = class_service.get_all_classes()
                count = sum(1 for c in classes if c.is_active)
                print(f"Active classes: {count}")
            elif choice == "4":
                total = subscription_service.total_income()
                print(f"Total income: {total:,}")
            elif choice == "5":
                return
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")



def manager_menu(user_service):
    # feature/halls-classes


    from gym.services.halls import HallService
    from gym.services.classes import ClassService
    
    hall_service = HallService()
    class_service = ClassService()
    
    from gym.services.subscriptions import SubscriptionService
    from gym.services.wallet import WalletService
    
    subscription_service = SubscriptionService()
    wallet_service = WalletService(user_service, subscription_service)

    while True:
        print("\n==== Manager Menu ====")
        print("1. User Management")
        print("2. Hall Management")
        print("3. Class Management")
        print("4. Subscription & Payments")
        print("5. View Reports")
        print("6. Logout")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            user_management_menu(user_service)
        elif choice == "2":
    # feature/halls-classes
            while True:
                print("\n===== Hall Management =====")
                print("1. Add Hall")
                print("2. Show All Halls")
                print("3. Back")

                hall_choice = input("Choose an option: ").strip()

                if hall_choice == "1":
                    hall_id = input("Hall ID: ").strip()
                    name = input("Hall name: ").strip()
                    equipment_str = input("Equipment (comma-separated): ").strip()
                    equipment = equipment_str.split(",") if equipment_str else []

                    try:
                        capacity = int(input("Capacity: ").strip())
                        hall = Hall(
                            id=hall_id,
                            name=name,
                            capacity=capacity,
                            equipment=equipment,
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
                    break

                else:
                    print("Invalid choice.")

        elif choice == "3":
            while True:
                print("\n===== Class Management =====")
                print("1. Add Class")
                print("2. Show All Classes")
                print("3. Back")

                class_choice = input("Choose an option: ").strip()

                if class_choice == "1":
                    class_id = input("Class ID: ").strip()
                    name = input("Class name: ").strip()
                    coach_id = input("Coach ID: ").strip()
                    hall_id = input("Hall ID: ").strip()

                    try:
                        capacity = int(input("Capacity: ").strip())
                        schedule = input("Schedule: ").strip()

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
                    break

                else:
                    print("Invalid choice.")


            
        
               
        elif choice == "4":
            subscription_management_menu(subscription_service, user_service)
        elif choice == "5":
            reports_menu(subscription_service, user_service, class_service)
        elif choice == "6":
            print("Logging out...")
            return