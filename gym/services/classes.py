import json
from gym.models import GymClass
from gym.storage import Storage

DATA_PATH = "data/gym_data.txt"
CLASSES_SECTION = "CLASSES"
class ClassService:
    def __init__(self):
        self.storage = Storage(DATA_PATH)
        self.classes = []
        self._load()
        
    def _load(self):
        
        self.classes = []

        if not self.storage.exists():
            return

        inside_section = False

        for line in self.storage.read_lines():
            text = line.strip()

            if text.startswith("[") and text.endswith("]"):
                inside_section = (text == f"[{CLASSES_SECTION}]")
                continue

            if not inside_section or not text:
                continue

            try:
                data = json.loads(text)
                gym_class = GymClass.from_dict(data)
                self.classes.append(gym_class)
            except (ValueError, TypeError, KeyError):
                print("Warning: invalid class record skipped.")

    def _save(self):
        
        lines = self.storage.read_lines()
        marker = f"[{CLASSES_SECTION}]"

        start = None
        end = None

        for i, line in enumerate(lines):
            if line.strip() == marker:
                start = i
                end = i + 1
                while end < len(lines) and not lines[end].strip().startswith("["):
                    end += 1
                break

        class_lines = [
            json.dumps(c.to_dict(), ensure_ascii=False)
            for c in self.classes
        ]

        if start is None:
            if lines and lines[-1].strip():
                lines.append("")
            lines.append(marker)
            lines.extend(class_lines)
        else:
            lines[start + 1:end] = class_lines

        self.storage.write_lines(lines)

    def add_class(self, gym_class):
        
        # Check for duplicate ID
        for existing_class in self.classes:
            if str(existing_class.id) == str(gym_class.id):
                print("This class ID already exists.")
                return

        # Generate new ID if "0"
        if str(gym_class.id) == "0":
            max_id = max(
                (int(c.id) for c in self.classes if str(c.id).isdigit()),
                default=0,
            )
            gym_class.id = str(max_id + 1)

        self.classes.append(gym_class)
        self._save()
        print("Class added successfully.")

    def get_all_classes(self):
        
        return list(self.classes)

    def find_by_id(self, class_id):
        
        for gym_class in self.classes:
            if str(gym_class.id) == str(class_id):
                return gym_class
        return None