from gym.models import Workout,Exercise
from gym.storage import load_data
from gym.exceptions import NotFoundError,PermissionError,ValidationError
from gym.validators import is_positive_integer

WORKOUTS_FILE = "gym_data/workouts.txt"

def workout_to_line(workout):
    #Workout --> String
    exercise_str= ";" .json(f"{ex.sets},{ex.reps},{ex.rest_time},{ex.description}"
        for ex in workout.exercises
    )
    return(
         f"{workout.id}|{workout.member_id}|{workout.class_id}|"
         f"{workout.coach_id}|{exercise_str}"
    )

def line_to_workout(line):
    "برعکس"
    parts = line.split("|")
    if len(parts) < 5:
        return None
     
    Workout_id = int(parts[0])
    member_id = int(parts[1])
    class_id = int(parts[2])
    coach_id =int(parts[3])
    exercises_str= parts[4]

    exercises = []

    if exercises_str.strip():
        for ex_str in exercises_str.split(";"):
            if not ex_str.strip():
                continue
            ex_parts = ex_str.split(",")
            if len(ex_parts) <4:
                continue
            exercises.append(Exercise(
                name = wx_parts[0],
                sets=int(ex_parts[1])
                reps=int(ex_parts[2])
                rest_time=int(ex_parts[3]) if len(ex_parts) > 3 else 0,
                description=ex_parts[4] if len(ex_parts) > 4 else "",
            ))
               
        return Workout(
            id= workout_id,
            member_id=memebr_id,
            class_id=class_id
            coach_id=coach_id
            exercises=exercises,
        )

def load_workouts():
    storage=Storage(WORKOUTS_FILE)
    workouts = []
    for line in storage.read_line():
        if not line.strip():
            continue
        w=line_to_workout(line)
        if w:
            workouts.append(w)
    return workouts


def save_workouts():
    storage = Storage(WORKOUTS_FILE)
    lines = [_workout_to_line(w) for w in workouts]
    storage.write_lines(lines)

def find_workouts(workouts,workout_id):
        for w in workouts:
            if w["id"] == workout_id:
                return w
        return None

def _next_id(workouts):
    if not workouts:
         return 1
    return max(w["id"] for w in workouts)+1

class WorkoutService:
    def __init__(self, class_sevice, registration_sevice, workouts = None):
        self.class_service = class_service
        self.registration_service = registration_service
        self.workouts = workouts if workouts is not None else self._load_all()
        self.next_id = max([w.id for w in self.workouts], default=0) + 1

    def load_all(self):
        storage = Storage(WORKOUTS_FILE)
        workouts = []
        for line in storage.read_line():
            if not line.strip():
                continue
            w = _line_to_workout(line)
            if w:
                workouts.append(w)
        return workouts
    
    def save_all(self):
        storage = Storage(WORKOUTS_FILE)
        lines = [workout_to_line(w) for w in self.workouts]
        storage.write_line(lines)

    def find_by_id(self, workout_id):
        for w in self.workouts:
            if str(w.id) == str(workout_id):
                return w
        return None

    def get_member_workout(self, member_id, class_id):
        for w in self.workouts:
            if (str(w.member_id) == str(member_id)
                    and str(w.class_id) == str(class_id)):
                return w
        return None
    
    def _class_belongs_to_coach(self, class_id, coach_id):
        classes = self.class_service.get_all_classes()
        for c in classes:
            if str(c.id) == str(class_id):
                return str(c.coach_id) == str(coach_id)
        return False

    def _is_registered(self, member_id, class_id):
        return self.registration_service.is_registered(member_id, class_id)
    
    def create_workout(self,coach_id ,class_id ,member_id):
        #چک کلاس مالک
        if not self._class_belongs_to_coach(class_id, coach_id):
            raise AccessDeniedError("این کلاس متعلق به شما نیست.")

        #چک ثبت نامی
        if not self._is_registered(member_id, class_id):
            raise ValidationError("این عضو در این کلاس ثبت‌نام نکرده است.")

        #چک تکراری نباشه
        if self.get_member_workout(member_id, class_id) is not None:
            raise DuplicateError("برای این عضو قبلاً برنامه ساخته شده است.")
        
        workout = Workout(
            id=self.next_id,
            member_id=member_id,
            class_id=class_id,
            coach_id=coach_id,
            exercises=[],
        )

        self.workouts.append(workout)
        self.next_id += 1
        self._save_all()

        return workout
    
    def add_exercise(self, workout_id, exercise_data):#اضافه تمیرین 
        workout = self.find_by_id(workout_id)
        if workout is None:
            raise NotFoundError("برنامه تمرینی پیدا نشد.")

        if not is_positive_integer(exercise_data.get("sets")):
            raise ValidationError("تعداد ست باید عدد صحیح مثبت باشه.")

        if not is_positive_integer(exercise_data.get("reps")):
            raise ValidationError("تعداد تکرار باید عدد صحیح مثبت باشه.")

        exercise = Exercise(
            name=exercise_data["name"],
            sets=int(exercise_data["sets"]),
            reps=int(exercise_data["reps"]),
            rest_time=int(exercise_data.get("rest_time", 0)),
            description=exercise_data.get("description", ""),
        )

        workout.add_exercise(exercise)
        self.save_all()
        return exercise
    
    def edit_exercise(self , workout_id, exercise_index, new_data):#با ایندکس برای ویرایش
        workout = self.find_by_id(workout_id)
        if workout is None :
            raise NotFoundError("برنامه تمرینی نیست")
        
        if not (0<= exercise_index < len(workout.exercises)):
            raise ValidationError("مشکل حرکت ایندکس")
        
        if not is_positive_integer(new_data.get("sets")):
            raise ValidationError("تعداد ست هاباید عدد مثبت باشه و صحیح")
        
        if not is_positive_integer(new_data.get("reps")):
            raise ValidationError("تعداد تکرار باید عدد صحیح مثبت باشه.")

        new_exercise = Exercise(
            name=new_data["name"],
            sets=int(new_data["sets"]),
            reps=int(new_data["reps"]),
            rest_time=int(new_data.get("rest_time", 0)),
            description=new_data.get("description", ""),
        )

        workout.edit_exercise(exercise_index, new_exercise)
        self._save_all()
        return new_exercise

    def remove_exercise(self, working_id, exercise_index):#حذف حرکت ایندکس
        workout = self.find_by_id(workout_id)
        if workout is None:
            raise NotFoundError("برنامه تمرینی پیدا نشد.")

        if not (0 <= exercise_index < len(workout.exercises)):
            raise ValidationError("ایندکس حرکت نامعتبر است.")

        workout.remove_exercise(exercise_index)
        self._save_all()

    def get_workout(self, workout_id):
        workout = self.find_by_id(workout_id)
        if workout in None:
            raise NotFoundError("برنامه تمیرین نیست")
        return workout
    
    def get_workout_by_coach(self,coach_id):
        return [w for w in self.workouts if str(w.coach_id) == str(coach_id)]
    
    def get_workouts_by_member(self,member_id):
        return [w for w in self.workouts if str(w.member_id) == str(member_id)]
