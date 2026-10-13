from gym.models import Workout,Exercise
from gym.storage import load_data
from gym.exceptions import NotFoundError,PermissionError,ValidationError

def load_workouts():
    return load_data("workouts")

def save_workouts():
    pass

def find_workouts(workouts,workout_id):
        for w in workouts:
            if w["id"] == workout_id:
                return w
        return None

def _next_id(workouts):
    if not workouts:
         return 1
    return max(w["id"] for w in workouts)+1