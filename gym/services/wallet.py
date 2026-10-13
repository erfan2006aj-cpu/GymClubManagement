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

 
    def get_balance(self, member_id):
        member = self._get_member(member_id)
        return member.wallet_balance

    def get_transactions(self, member_id=None):
        result = []
        for trans in self._transactions:
            if member_id is None or trans.member_id == member_id:
                result.append(trans)

        return sorted(result, key=lambda t: t.date, reverse=True)

    
    def charge_wallet(self, member_id, amount, card, exp_month, exp_year, password, cvv2):

        try:
            amount = float(amount)
            exp_month = int(exp_month)
            exp_year = int(exp_year)
        except (TypeError, ValueError):
            raise ValidationError("ورودی‌ کارت نامعتبر")

        if amount <= 0:
            raise ValidationError("مبلغ باید بیشتر از صفر باشد")

        member = self._get_member(member_id)

        api = BankAPI()
        try:
            payment_id = api.pay(card, exp_month, exp_year, password, cvv2, amount)
        except ValueError as error:
            raise ValidationError(f"پرداخت ناموفق: {error}")

        trans = self._record(
            member_id=member_id,
            tx_type=Transaction.TYPE_CHARGE,
            amount=amount,
            description="شارژ کیف پول",
            tracking_number=str(payment_id),
        )

        member.wallet_balance += amount
        self.user_service.save()

        return trans


    def pay_subscription(self, member_id, plan_type):

            member = self._get_member(member_id)

            if self.subscription_service is None:
                raise ValidationError("اشتراک دردسترس نیست!")

            try:
                price = self.subscription_service.get_plan_price(plan_type)
                label = self.subscription_service.get_plan_label(plan_type)
            except (KeyError, ValueError):
                raise ValidationError("اشتراک نامعتبر")

            if member.wallet_balance < price:
                raise InsufficientBalanceError("موجودی کافی نیست")

            member.wallet_balance -= price

            try:
                tub = self.subscription_service.create_subscription(
                    member_id=member_id,
                    kind=plan_type,
                    amount=price,
                )
            except Exception:
                member.wallet_balance += price
                raise

            self.user_service.save()

            trans = self._record(
                member_id=member_id,
                tx_type=Transaction.TYPE_PAYMENT,
                amount=price,
                description=f"خرید {label}",
                tracking_number=str(sub.tracking_number),
            )

            return trans