
import re

from gym.models import Coach, Member


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
