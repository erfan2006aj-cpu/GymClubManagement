from datetime import datetime, timedelta

from gym.exceptions import ValidationError
from gym.models import Subscription
from gym.storage import Storage
import random


DATA_PATH = "data/gym_data.txt"
SUBS_SECTION = "SUBSCRIPTIONS"
SPLITTER = "|"
NUM_PARTS = 8

PLANS = {
    "1month": {"name": "یک ماهه", "days": 30, "cost": 500000},
    "3month": {"name": "سه ماهه", "days": 90, "cost": 1350000},
    "6month": {"name": "شش ماهه", "days": 180, "cost": 2500000},
}


class SubscriptionService:
    def __init__(self):
        self.storage = Storage(DATA_PATH)
        self._subscriptions = []
        self._load()


    def list_plans(self):
        return list(PLANS.items())

    def get_plan_price(self, kind):
        if kind not in PLANS:
            raise ValidationError("نوع اشتراک نامعتبر")
        return PLANS[kind]["cost"]

    def get_plan_label(self, kind):
        if kind not in PLANS:
            raise ValidationError("نوع اشتراک نامعتبر")
        return PLANS[kind]["name"]


    def create_subscription(self, member_id, kind, amount):
        if kind not in PLANS:
            raise ValidationError("نوع اشتراک نامعتبر")

        start = datetime.now()
        old = self.get_active_subscription(member_id)
        if old:
            start = old.end_date

        end = start + timedelta(days=PLANS[kind]["days"])

        sub = Subscription(
            id=self._next_id(),
            member_id=member_id,
            subscription_type=kind,
            amount=amount,
            start_date=start,
            end_date=end,
            tracking_number=self._new_tracking(),
            is_active=True,
        )
        self._subscriptions.append(sub)
        self._save(sub)
        return sub


    def get_active_subscription(self, member_id):
        for sub in self._subscriptions:
            if sub.member_id == member_id and sub.is_active and not sub.is_expired():
                return sub
        return None

    def has_active_subscription(self, member_id):
        return self.get_active_subscription(member_id) is not None

    def get_member_status(self, member_id):
        found = [s for s in self._subscriptions if s.member_id == member_id]
        if not found:
            return Subscription.STATUS_NONE
        for sub in found:
            if sub.is_active and not sub.is_expired():
                return Subscription.STATUS_ACTIVE
        return Subscription.STATUS_EXPIRED


    def list_all(self):
        return list(self._subscriptions)

    def list_by_member(self, member_id):
        return [s for s in self._subscriptions if s.member_id == member_id]

    def total_income(self):
        total = 0
        for sub in self._subscriptions:
            total += sub.amount
        return total


    def _load(self):
        self._subscriptions = []
        if not self.storage.exists():
            return

        lines = self.storage.read_lines()
        inside = False
        number = 0

        for line in lines:
            number = number + 1
            t = line.strip()

            if t.startswith("[") and t.endswith("]"):
                inside = (t == "[" + SUBS_SECTION + "]")
                continue

            if not inside:
                continue

            if t == "":
                continue

            try:
                self._subscriptions.append(self._from_line(t))
            except Exception:
                print(f"خط {number} نامعتبره")

    def _save(self, sub):
        line = self._to_line(sub)
        lines = self.storage.read_lines()
        mark = "[" + SUBS_SECTION + "]"

        pos = None
        for i in range(len(lines)):
            if lines[i].strip() == mark:
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith("["):
                    j += 1
                pos = j
                break

        if pos is None:
            if lines and lines[-1].strip():
                lines.append("")
            lines.append(mark)
            lines.append(line)
        else:
            lines.insert(pos, line)

        self.storage.write_lines(lines)

    def _to_line(self, sub):
        fields = [
            str(sub.id),
            str(sub.member_id),
            sub.subscription_type,
            str(sub.amount),
            sub.start_date.isoformat(),
            sub.end_date.isoformat(),
            sub.tracking_number,
            str(sub.is_active),
        ]
        return SPLITTER.join(fields)

    def _from_line(self, line):
        f = line.split(SPLITTER)
        if len(f) != NUM_PARTS:
            raise ValidationError("invalid field count")

        return Subscription(
            id=int(f[0]),
            member_id=int(f[1]),
            subscription_type=f[2],
            amount=float(f[3]),
            start_date=datetime.fromisoformat(f[4]),
            end_date=datetime.fromisoformat(f[5]),
            tracking_number=f[6],
            is_active=f[7] == "True",
        )


    def _next_id(self):
        if len(self._subscriptions) == 0:
            return 1

        biggest = 0
        for sub in self._subscriptions:
            if sub.id > biggest:
                biggest = sub.id

        return biggest + 1

    def _new_tracking(self):
        while True:
            number = random.randint(100000, 999999)
            if not any(s.tracking_number == str(number) for s in self._subscriptions):
                return str(number)