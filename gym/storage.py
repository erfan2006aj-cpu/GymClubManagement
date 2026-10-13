import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def _get_file_path(name):
    return os.path.join(DATA_DIR, f"{name}.json")

def load_data(name):
   path = _get_file_path(name)

    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(name, data):
   if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    path = _get_file_path(name)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
