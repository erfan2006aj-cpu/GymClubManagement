from datetime import datetime
from bank.Bank import API as BankAPI
from gym.exceptions import (
    NotFoundError,
    ValidationError,
    AccountDisabledError,
    InsufficientBalanceError,
)
from gym.models import Member, Transaction
from gym.storage import Storage


DATA_PATH = "data/gym_data.txt"
WALLET_SECTION = "TRANSACTIONS"
SPLITTER = "|"
NUM_PARTS = 7


class WalletService:
    def __init__(self, user_service, subscription_service=None):
        self.user_service = user_service
        self.subscription_service = subscription_service
        self.storage = Storage(DATA_PATH)
        self._transactions = []
        self._load()


    def _to_line(self, trans):
        note = trans.description
        note = note.replace(SPLITTER, " ")
        note = note.replace("\n", " ")

        fields = [
            str(trans.id),
            str(trans.member_id),
            trans.transaction_type,
            str(trans.amount),
            trans.date.isoformat(),
            note,
            str(trans.tracking_number),
        ]
        return SPLITTER.join(fields)

    def _from_line(self, line):
        fields = line.split(SPLITTER)
        if len(fields) != NUM_PARTS:
            raise ValidationError("invalid field count: " + str(len(fields)))

        trans = Transaction(
            id=int(fields[0]),
            member_id=int(fields[1]),
            transaction_type=fields[2],
            amount=float(fields[3]),
            date=datetime.fromisoformat(fields[4]),
            description=fields[5],
            tracking_number=fields[6],
        )
        return trans


    def _load(self):
        self._transactions = []

        if not self.storage.exists():
            return

        all_lines = self.storage.read_lines()
        in_section = False
        number = 0

        for line in all_lines:
            number = number + 1
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                in_section = (stripped == "[" + WALLET_SECTION + "]")
                continue

            if not in_section:
                continue

            if stripped == "":
                continue

            try:
                trans = self._from_line(stripped)
                self._transactions.append(trans)
            except (ValueError, KeyError):
                print(f"خط  {number} نامعتبره")

    def _save(self, trans):
        line = self._to_line(trans)

        all_lines = self.storage.read_lines()
        target = "[" + WALLET_SECTION + "]"

        insert_at = None
        for i in range(len(all_lines)):
            if all_lines[i].strip() == target:
                j = i + 1
                while j < len(all_lines) and not all_lines[j].strip().startswith("["):
                    j = j + 1
                insert_at = j
                break

        if insert_at is None:
            if all_lines and all_lines[-1].strip():
                all_lines.append("")
            all_lines.append(target)
            all_lines.append(line)
        else:
            all_lines.insert(insert_at, line)

        self.storage.write_lines(all_lines)

    def _next_id(self):
        if len(self._transactions) == 0:
            return 1

        biggest = 0
        for trans in self._transactions:
            if trans.id > biggest:
                biggest = trans.id

        return biggest + 1

    def _get_member(self, member_id):
        member = self.user_service.find_by_id(member_id)

        if member is None:
            raise NotFoundError("عضو پیدا نشد")

        if not isinstance(member, Member):
            raise ValidationError("کاربر عضو نیست")

        if not member.is_active:
            raise AccountDisabledError("حساب غیرفعال است.")

        return member

    def _record(self, member_id, tx_type, amount, description, tracking_number):
        trans = Transaction(
            id=self._next_id(),
            member_id=member_id,
            transaction_type=tx_type,
            amount=amount,
            date=datetime.now(),
            description=description,
            tracking_number=tracking_number,
        )

        self._transactions.append(trans)

        try:
            self._save(trans)
        except OSError:
            self._transactions.remove(trans)
            raise

        return trans