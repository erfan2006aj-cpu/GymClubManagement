import re
import json
from gym.models import Coach, Member, Manager
from gym.storage import Storage
ALLOWED_ROLES = {"member", "coach"}
def is_valid_email(email):
    if not isinstance(email, str):
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email.strip()) is not None


def is_username_available(username, existing_users):
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username cannot be empty.")

    username = username.strip().casefold()

    for user in existing_users:
        if user.username.casefold() == username:
            return False

    return True


def add_user(
    name,
    username,
    password,
    email,
    role,
    existing_users=None,
    is_active=True,
):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name cannot be empty.")
    name = name.strip()

    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username cannot be empty.")
    username = username.strip()

    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password cannot be empty.")
    password = password.strip()

    if not is_valid_email(email):
        raise ValueError("Invalid email address.")
    email = email.strip()

    if not isinstance(role, str):
        raise ValueError("Invalid user role.")

    role = role.strip().casefold()

    if role not in ALLOWED_ROLES:
        raise ValueError("Role must be 'member' or 'coach'.")

    if existing_users is not None:
        if not is_username_available(username, existing_users):
            raise ValueError("Username already exists.")

    if role == "member":
        user = Member(
            id=None,
            name=name,
            username=username,
            password=password,
            email=email,
            is_active=is_active,
        )
    else:
        user = Coach(
            id=None,
            name=name,
            username=username,
            password=password,
            email=email,
            is_active=is_active,
        )

    return user

def activate_user(user):
    user.activate()
    return user
def deactivate_user(user):
    user.deactivate()
    return user

def update_user(
    user,
    name=None,
    username=None,
    password=None,
    email=None,
    existing_users=None,
):
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty.")
        user.name = name.strip()

    if username is not None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username cannot be empty.")

        username = username.strip()

        if existing_users is not None:
            for other_user in existing_users:
                if other_user is not user:
                    if other_user.username.casefold() == username.casefold():
                        raise ValueError("Username already exists.")

        user.username = username
    if email is not None:
        if not is_valid_email(email):
            raise ValueError("Invalid email address.")
        user.email = email.strip()
    if password is not None:
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password cannot be empty.")
        user.password = password.strip()

    return user

def get_user_by_username(username, existing_users):
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username cannot be empty.")

    username = username.strip().casefold()

    for user in existing_users:
        if user.username.casefold() == username:
            return user

    return None


def get_all_users(existing_users):
    return list(existing_users)

import json

DATA_PATH = "data/gym_data.txt"
USERS_SECTION = "USERS"


class UserService:
    def __init__(self):
        self.storage = Storage(DATA_PATH)
        self.users = []
        self._load()

    def _load(self):
        """Load users from the text file."""
        self.users = []

        if not self.storage.exists():
            return

        inside_section = False

        for line in self.storage.read_lines():
            text = line.strip()

            if text.startswith("[") and text.endswith("]"):
                inside_section = text == f"[{USERS_SECTION}]"
                continue

            if not inside_section or not text:
                continue

            try:
                data = json.loads(text)
                role = data.get("role")

                if role == "member":
                    user = Member.from_dict(data)
                elif role == "coach":
                    user = Coach.from_dict(data)
                else:
                    continue

                self.users.append(user)

            except (ValueError, TypeError, KeyError):
                print("Warning: Invalid user record skipped.")

    def _save(self):
        """Save users without deleting other text-file sections."""
        lines = self.storage.read_lines()
        marker = f"[{USERS_SECTION}]"

        start = None
        end = None

        for i, line in enumerate(lines):
            if line.strip() == marker:
                start = i
                end = i + 1

                while (
                    end < len(lines)
                    and not lines[end].strip().startswith("[")
                ):
                    end += 1

                break

        user_lines = [
            json.dumps(user.to_dict(), ensure_ascii=False)
            for user in self.users
        ]

        if start is None:
            if lines and lines[-1].strip():
                lines.append("")

            lines.append(marker)
            lines.extend(user_lines)
        else:
            lines[start + 1:end] = user_lines

        self.storage.write_lines(lines)

    def list_all(self):
        return list(self.users)

    def find_by_id(self, user_id):
        for user in self.users:
            if str(user.id) == str(user_id):
                return user
        return None

    def find_by_username(self, username):
        return get_user_by_username(username, self.users)

    def add(self, name, username, password, email, role):
        user = add_user(
            name=name,
            username=username,
            password=password,
            email=email,
            role=role,
            existing_users=self.users,
        )

        user.id = max(
            (
                int(item.id)
                for item in self.users
                if item.id is not None
            ),
            default=0,
        ) + 1

        self.users.append(user)

        try:
            self._save()
        except OSError:
            self.users.remove(user)
            raise

        return user

    def update(self, user, **changes):
        old_data = user.to_dict()

        update_user(
            user,
            existing_users=self.users,
            **changes,
        )

        try:
            self._save()
        except OSError:
            restored = (
                Member.from_dict(old_data)
                if user.role == "member"
                else Coach.from_dict(old_data)
            )

            user.__dict__.clear()
            user.__dict__.update(restored.__dict__)
            raise

        return user

    def set_active(self, user, is_active):
        old_status = user.is_active
        user.is_active = is_active

        try:
            self._save()
        except OSError:
            user.is_active = old_status
            raise

        return user
