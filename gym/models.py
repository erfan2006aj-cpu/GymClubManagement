from dataclasses import dataclass, field , asdict
from datetime import datetime


class User:
    def __init__(
        self,
        id,
        name,
        username,
        password,
        email,
        role,
        is_active=True
    ):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.is_active = is_active

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            role=data["role"],
            is_active=data.get("is_active", True),
        )


class Manager(User):
    def __init__(
        self,
        id,
        name,
        username,
        password,
        email,
        is_active=True
    ):
        super().__init__(
            id=id,
            name=name,
            username=username,
            password=password,
            email=email,
            role="manager",
            is_active=is_active,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            is_active=data.get("is_active", True),
        )

class Coach(User):
    def __init__(
        self,
        id,
        name,
        username,
        password,
        email,
        is_active=True
    ):
        super().__init__(
            id=id,
            name=name,
            username=username,
            password=password,
            email=email,
            role="coach",
            is_active=is_active,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            is_active=data.get("is_active", True),
        )

class Member(User):
    def __init__(
        self,
        id,
        name,
        username,
        password,
        email,
        wallet_balance=0,
        is_active=True
    ):
        super().__init__(
            id=id,
            name=name,
            username=username,
            password=password,
            email=email,
            role="member",
            is_active=is_active,
        )
        self.wallet_balance = wallet_balance

    def increase_balance(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.wallet_balance += amount

    def decrease_balance(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if amount > self.wallet_balance:
            raise ValueError("Insufficient wallet balance.")
        self.wallet_balance -= amount

    def to_dict(self):
        data = super().to_dict()
        data["wallet_balance"] = self.wallet_balance
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            wallet_balance=data.get("wallet_balance", 0),
            is_active=data.get("is_active", True),
        )


@dataclass
class Subscription:
    id:int
    member_id: int
    subscription_type:str
    amount:float
    start_date: datetime
    end_date:datetime
    tracking_number: str
    is_active: bool = True

    STATUS_ACTIVE = "ACTIVE"
    STATUS_EXPIRED = "EXPIRED"
    STATUS_NONE = "NO SUBSCRIPTION"

    def is_expired(self):
        return self.end_date < datetime.now()

    def status(self):
        if self.is_expired():
            return self.STATUS_EXPIRED
        else:
            return self.STATUS_ACTIVE

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "subscription_type": self.subscription_type,
            "amount": self.amount,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "tracking_number": self.tracking_number,
            "is_active": self.is_active,
        }   

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data["id"]),
            member_id=int(data["member_id"]),
            subscription_type=str(data["subscription_type"]),
            amount=float(data["amount"]),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            tracking_number=str(data["tracking_number"]),
            is_active=str(data["is_active"]).lower() == "true",
        )


@dataclass
class Transaction:
    id:int
    member_id:int
    transaction_type: str
    amount:float
    date: datetime
    description: str
    tracking_number: str

    TYPE_CHARGE = "charge"
    TYPE_PAYMENT = "payment"
    TYPE_REFUND = "refund"
    VALID_TYPES = ("charge", "payment", "refund")

    def is_valid_type(self):
        return self.transaction_type in self.VALID_TYPES

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "description": self.description,
            "tracking_number": self.tracking_number,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data["id"]),
            member_id=int(data["member_id"]),
            transaction_type=str(data["transaction_type"]),
            amount=float(data["amount"]),
            date=datetime.fromisoformat(data["date"]),
            description=str(data["description"]),
            tracking_number=str(data["tracking_number"]),
        )


@dataclass
class Registration:
    id: int
    class_id: int
    member_id: int
    tracking_number: str
    is_active: bool = True
    registration_date: datetime = field(default_factory=datetime.now)

    def cancel(self) -> None:
        self.is_active = False
        
    def activate(self) -> None:
        self.is_active = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dictionary_data : dict) -> "Registration":
        return cls(**dictionary_data)


@dataclass
class Exercise:
    name: str
    sets: int
    reps: int
    rest_time: int = 0
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "sets": self.sets,
            "reps": self.reps,
            "rest_time": self.rest_time,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Exercise":
        return cls(
            name=data["name"],
            sets=int(data["sets"]),
            reps=int(data["reps"]),
            rest_time=int(data.get("rest_time", 0)),
            description=data.get("description", ""),
        )


@dataclass
class Workout:
    id: int
    member_id: int
    class_id: int
    coach_id: int
    exercises: list[Exercise] = field(default_factory=list)

    def add_exercise(self, exercise: Exercise) -> None:
        self.exercises.append(exercise)

    def remove_exercise(self, index: int) -> None:
        if not 0 <= index < len(self.exercises):
            raise IndexError("Exercise index out of range.")
        self.exercises.pop(index)

    def edit_exercise(self, index: int, new_exercise: Exercise) -> None:
        if not 0 <= index < len(self.exercises):
            raise IndexError("Exercise index out of range.")
        self.exercises[index] = new_exercise

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "member_id": self.member_id,
            "class_id": self.class_id,
            "coach_id": self.coach_id,
            "exercises": [
                exercise.to_dict() for exercise in self.exercises
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Workout":
        return cls(
            id=int(data["id"]),
            member_id=int(data["member_id"]),
            class_id=int(data["class_id"]),
            coach_id=int(data["coach_id"]),
            exercises=[
                Exercise.from_dict(item)
                for item in data.get("exercises", [])
            ],
        )

@dataclass
class Hall:
    id: str
    name: str
    capacity: int
    equipment: list[str] = field(default_factory=list)
    is_active: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "equipment": self.equipment,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Hall":
        return cls(
            id=data["id"],
            name=data["name"],
            capacity=int(data["capacity"]),
            equipment=data.get("equipment", []),
            is_active=data.get("is_active", True),
        )


@dataclass
class GymClass:
    id: str
    name: str
    coach_id: str
    hall_id: str
    capacity: int
    schedule: str
    is_active: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "coach_id": self.coach_id,
            "hall_id": self.hall_id,
            "capacity": self.capacity,
            "schedule": self.schedule,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GymClass":
        return cls(
            id=data["id"],
            name=data["name"],
            coach_id=data["coach_id"],
            hall_id=data["hall_id"],
            capacity=int(data["capacity"]),
            schedule=data["schedule"],
            is_active=data.get("is_active", True),
            )