import json
from gym.models import Hall
from gym.storage import Storage

DATA_PATH="data/gym_data.txt"
HALLS_SECTION = "HALLS"

class HallService:
    def __init__(self):
        self.storage = Storage(DATA_PATH)
        self.halls = []
        self._load()

    def _load(self):
        
        self.halls = []

        if not self.storage.exists():
            return

        inside_section = False

        for line in self.storage.read_lines():
            text = line.strip()

            if text.startswith("[") and text.endswith("]"):
                inside_section = (text == f"[{HALLS_SECTION}]")
                continue

            if not inside_section or not text:
                continue

            try:
                data = json.loads(text)
                hall = Hall.from_dict(data)
                self.halls.append(hall)
            except (ValueError, TypeError, KeyError):
                print("Warning: invalid hall record skipped.")

    def _save(self):
        
        lines = self.storage.read_lines()
        marker = f"[{HALLS_SECTION}]"

        start = None
        end = None

        for i, line in enumerate(lines):
            if line.strip() == marker:
                start = i
                end = i + 1
                while end < len(lines) and not lines[end].strip().startswith("["):
                    end += 1
                break

        hall_lines = [
            json.dumps(hall.to_dict(), ensure_ascii=False)
            for hall in self.halls
        ]

        if start is None:
            if lines and lines[-1].strip():
                lines.append("")
            lines.append(marker)
            lines.extend(hall_lines)
        else:
            lines[start + 1:end] = hall_lines

        self.storage.write_lines(lines)

    def add_hall(self, hall):
        # feature/halls-classes
        all_halls = self.get_all_halls()
        for existing_hall in all_halls:
            if str(existing_hall.id) == str(hall.id):
                print("This hall ID already exists.")
                return

        
        if str(hall.id) == "0":
            max_id = max(
                (int(h.id) for h in self.halls if str(h.id).isdigit()),
                default=0,
            )
            hall.id = str(max_id + 1)

        self.halls.append(hall)
        self._save()
        print("Hall added successfully.")

    def get_all_halls(self):
        """Get all halls."""
        return list(self.halls)

    def find_by_id(self, hall_id):
        """Find a hall by its ID."""
        for hall in self.halls:
            if str(hall.id) == str(hall_id):
                return hall
        return None

    def set_active(self, hall, is_active):
        hall.is_active = is_active
        self._save()
        return hall