from gym.exceptions import NotFoundError,ValidationError,AccessDeniedError,DuplicateError
from gym.services.workout import WorkoutService
from gym.services.classes import ClassService


def print_header(title):
    print("\n"+"="*45)
    print(f" {title}")
    print("=" * 45)

def view_my_classes(coach_id , class_service):
    print_header("My Classes")
    all_classes = class_service.get_all_classes()
    my_classes = [c for c in all_classes if str(c.coach_id) == str(coach_id)]

    if not my_classes:
        print("You have no classes.")
        return
    
    for i,c in enumerate(my_classes,1):
        print(f"\n [ {i}] {c.name}")
        print(f"    ID : {c.id}")
        print(f"    Schedule : {c.Schedule}")
        print(f"    Capacity : {c.capacity}")
        print(f"    Active   : {c.is_active}")

def select_class(coach_id , class_service):
    all_classes = class_service.get_all_classes()
    my_classes = [c for c in all_classes if str(c.coach_id) == str(coach_id)]

    if not my_classes:
        print("You have no classes.")
        return None

    print("\n --- select a Class -- ")
    for i,c in enumerate(my_classes,1):
        print(f" {i}.{c.name}  (ID : {c.id})")

    choice = input("choose a class number(0 to cancel):")
    if choice == "0":
        return None
    
    try:
        index = int(choice) -1
        if 0<= index<len(my_classes):
            return my_classes[index]
        print("Invalid class number.")
        return None
    except ValueError:
        print("Please enter a valid class number.")
        return None
    
def select_member(class_id,registration_service):
    try:
        registrations = registration_service.get_class_members(class_id)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    if not registrations:
        print("No members registered in this class.")
        return None
    
    print("\n --- Select a Number ---")
    for i,r in enumerate(registrations,1):
        print(f" {i}.Member ID : {r.member_id} (Tracking: {r.tracking_number})")

        choice = input("Choose a member number (0 to cancel): ").strip()
    if choice == "0":
        return None
    
    try:
        index = int(choice)-1
        if 0 <= index < len(registrations):
            return registrations[index]
        print("Invalid memmber number.")
        return None
    except ValueError:
        print("Please enter a valid number.")
        return None
    
def vew_workout(workout):
    print(f"\n--- Workout ID: {workout.id} ---")
    print(f"    Member ID : {workout.member_id}")
    print(f"    Class ID  : {workout.class_id}")
    print(f"    Coach ID  : {workout.coach_id}")

    if not workout.exercises:
        print("No exercises recorded yet.")
        return

    print("\n    Exercises:")
    for i, ex in enumerate(workout.exercises, 1):
        print(f"      [{i}] {ex.name}")
        print(f"          Sets   : {ex.sets}")
        print(f"          Reps   : {ex.reps}")
        print(f"          Rest   : {ex.rest_time}s")
        print(f"          Desc   : {ex.description or '-'}")

def get_exercise_input():
    name=input("Exercise name : ").strip()
    if not name:
        print("Exercise name cannot be empty.")
        return None
    
    sets_str = input("Sets: ").strip()
    reps_str = input("Reps: ").strip()
    rest_str = input("Rest time (seconds, default 0): ").strip() or "0"
    description = input("Description (optional): ").strip()

    return {
        "name": name,
        "sets": sets_str,
        "reps": reps_str,
        "rest_time": rest_str,
        "description": description,
    }

def create_workout_flow(coach_id, workout_service, class_service, registration_service):
    gym_class = select_class(coach_id, class_service)
    if gym_class is None:
        return

    member_reg = select_member(gym_class.id, registration_service)
    if member_reg is None:
        return

    try:
        workout = workout_service.create_workout(
            coach_id=coach_id,
            class_id=gym_class.id,
            member_id=member_reg.member_id,
        )
        print(f"\nWorkout created successfully (ID: {workout.id})")
    except (AccessDeniedError, ValidationError, DuplicateError) as e:
        print(f"Error: {e}")

def view_workouts_flow(coach_id, workout_service):
    workouts = workout_service.get_workouts_by_coach(coach_id)

    if not workouts:
        print("No workout found.")
        return

    for w in workouts:
        view_workout(w)

def add_exercise_flow(workout_service):
    workout_id = input("Workout ID: ").strip()
    if not workout_id:
        return

    exercise_data = get_exercise_input()
    if exercise_data is None:
        return

    try:
        workout_service.add_exercise(int(workout_id), exercise_data)
        print("Exercise added successfully.")
    except (NotFoundError, ValidationError) as e:
        print(f"Error: {e}")
    except ValueError:
        print("Invalid workout ID")

def edit_exercise_flow(workout_service):
    workout_id = input("Workout ID: ").strip()
    if not workout_id:
        return

    try:
        workout = workout_service.get_workout(int(workout_id))
        view_workout(workout)

        index_str = input("Exercise number to edit (1-based): ").strip()
        index = int(index_str) - 1

        new_data = get_exercise_input()
        if new_data is None:
            return

        workout_service.edit_exercise(int(workout_id), index, new_data)
        print("Exercise edited successfully.")
    except (NotFoundError, ValidationError) as e:
        print(f"Error {e}")
    except ValueError:
        print("Invalid input")

def remove_exercise_flow(workout_service):
    workout_id = input("Workout ID: ").strip()
    if not workout_id:
        return

    try:
        workout = workout_service.get_workout(int(workout_id))
        view_workout(workout)

        index_str = input("Exercise number to remove (1-based): ").strip()
        index = int(index_str) - 1

        workout_service.remove_exercise(int(workout_id), index)
        print("Exercise removed successfully.")
    except (NotFoundError, ValidationError) as e:
        print(f"Error {e}")
    except ValueError:
        print("Invalid input.")

def manage_workouts(coach_id, workout_service, class_service, registration_service):
    while True:
        print_header("Manage Workout Plans")
        print("1. Create Workout for a Member")
        print("2. View Workouts")
        print("3. Add Exercise to a Workout")
        print("4. Edit Exercise in a Workout")
        print("5. Remove Exercise from a Workout")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_workout_flow(coach_id, workout_service, class_service, registration_service)
        elif choice == "2":
            view_workouts_flow(coach_id, workout_service)
        elif choice == "3":
            add_exercise_flow(workout_service)
        elif choice == "4":
            edit_exercise_flow(workout_service)
        elif choice == "5":
            remove_exercise_flow(workout_service)
        elif choice == "6":
            return
        else:
            print("Invalid choice.")

def trainer_menu(coach_id, workout_service, class_service, registration_service):
    while True:
        print_header("Trainer Menu")
        print("1. View My Classes")
        print("2. Manage Workout Plans")
        print("3. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_my_classes(coach_id, class_service)
        elif choice == "2":
            manage_workouts(coach_id, workout_service, class_service, registration_service)
        elif choice == "3":
            print("Logging out...")
            return
        else:
<<<<<<< HEAD
            print("Invalid Choice. Please try again.")
            
=======
            print("انتخاب نامعتبر است ولی لطفا دوباره تلاش کنید.")
            
>>>>>>> 61fde75 (fix(workout, trainer_menu): fix typos and bugs)
