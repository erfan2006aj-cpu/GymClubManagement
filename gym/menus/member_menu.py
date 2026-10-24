from gym.services.registrations import Registration_service
class MemberMenu:
    def __init__(self, member, registration_service: Registration_service,class_service, subscription_service,wallet_service=None,user_service=None, workout_service=None):
        self.member = member
        self.registration_service = registration_service
        self.class_service = class_service
        self.subscription_service = subscription_service
        self.wallet_service = wallet_service
        self.user_service = user_service
        self.workout_service = workout_service

    def show(self):
        while True:
            try:
                print("\n ====Member Menu====")
                print(f" Balance: {self.member.wallet_balance}")
                print("-" * 25)
                print("1. Show available classes")
                print("2. Register in class")
                print("3. Cancel registration")
                print("4. My registrations")
                print("5. My subscription status")
                print("6. Buy subscription")
                print("7. Charge wallet")
                print("8. My transactions")
                print("9. My Workout Plan")
                print("0. Exit")
                choice = input("Choose an option: ")

                if choice == "1":
                    self.list_available_classes()
                elif choice == "2":
                    self.register_to_class()
                elif choice == "3":
                    self.cancel_registration()
                elif choice == "4":
                    self.show_my_registrations()
                elif choice == "5":
                    self.show_subscription_status()
                elif choice == "6":
                    self.buy_subscription()
                elif choice == "7":
                    self.charge_wallet()
                elif choice == "8":
                    self.show_transactions()
                elif choice == "9":
                    self.show_workout_plan()

                elif choice == "0":
                    break
                else:
                    print(f"'{choice}' is not a valid option. Please choose 0-8.")
            except KeyboardInterrupt:
                print("\nReturning to main menu...")
                break
            except Exception as e:
                print(f"\n[ERROR] : {e}")

    def list_available_classes(self):
        try:
            classes = self.class_service.get_all_classes()
            found = False
            for c in classes:
                if not c.is_active:
                    continue
                registered = len(self.registration_service.get_class_members(c.id))
                if registered >= c.capacity:
                    continue
                remaining = c.capacity - registered
                print(f"ID= {c.id} | {c.name} | capacity: {remaining}")
                found = True
            if not found:
                print("No available classes found.")
        except Exception as e:
            print(f"Error: {e}")

    def register_to_class(self):
        try:
            class_id = int(input("Class Id :"))
            reg = self.registration_service.register(self.member, class_id, self.subscription_service)
            if self.user_service:
                self.user_service._save()
            print(f"Registration was successful | tracking number : {reg.tracking_number}")
        except ValueError as e:
            print(f"Error : {e}")

    def cancel_registration(self):
        try:
            class_id = int(input("Class Id :"))
            reg = self.registration_service.cancel_registration(self.member.id, class_id)
            print(f"Cancellation was successful | tracking number : {reg.tracking_number}")
        except ValueError as e:
            print(f"Error : {e}")

    def show_my_registrations(self):
        regs = self.registration_service.get_member_registrations(self.member.id)
        if not regs:
            print("You do not have any active registration")
            return
        for r in regs:
            print(f"Class Id : {r.class_id} | Tracking number : {r.tracking_number} "
                  f"| Date : {r.registration_date:%Y-%m-%d %H:%M}")

    def charge_wallet(self):
        if self.wallet_service is None:
            print("Wallet service not available.")
            return

        print("\n--- Wallet Charge ---")
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("Error: Amount must be positive.")
                return

            card = input("Card number: ").strip()
            exp_month = int(input("Exp month: "))
            exp_year = int(input("Exp year: "))
            password = input("Card password: ").strip()
            cvv2 = input("CVV2: ").strip()

            trans = self.wallet_service.charge_wallet(
                member_id=self.member.id,
                amount=amount,
                card=card,
                exp_month=exp_month,
                exp_year=exp_year,
                password=password,
                cvv2=cvv2,
            )

            print(f"\nOK! Wallet charged. Balance: {self.member.wallet_balance}")
            print(f"Tracking number: {trans.tracking_number}")

        except ValueError as e:
            print(f"Error: {e}")

    def show_subscription_status(self):
        status = self.subscription_service.get_member_status(self.member.id)
        print(f"Subscription status: {status}")

        active = self.subscription_service.get_active_subscription(self.member.id)
        if active:
            print(f"  Type      : {active.subscription_type}")
            print(f"  Start     : {active.start_date:%Y-%m-%d %H:%M}")
            print(f"  End       : {active.end_date:%Y-%m-%d %H:%M}")
            print(f"  Tracking  : {active.tracking_number}")
            print(f"  Amount    : {active.amount}")

    def buy_subscription(self):
        if self.subscription_service.has_active_subscription(self.member.id):
            print("You already have an active subscription.")
            return

        print("\nAvailable plans:")
        for kind, plan in self.subscription_service.list_plans():
            print(f"  {kind}: {plan['name']} - {plan['cost']}")

        kind = input("Choose plan (1month/3month/6month): ").strip()

        try:
            price = self.subscription_service.get_plan_price(kind)
        except ValueError as e:
            print(f"Error: {e}")
            return

        if self.member.wallet_balance < price:
            print(f"Error: Insufficient balance.")
            print(f"  Needed   : {price}")
            print(f"  Available: {self.member.wallet_balance}")
            return

        self.member.wallet_balance -= price

        if self.user_service:
            self.user_service.save()

        try:
            sub = self.subscription_service.create_subscription(
                member_id=self.member.id,
                kind=kind,
                amount=price,
            )
            print(f"OK! Subscription active until {sub.end_date:%Y-%m-%d %H:%M}")
            print(f"Tracking number: {sub.tracking_number}")

            trans = self.wallet_service._record(
                member_id=self.member.id,
                tx_type="payment",
                amount=price,
                description=f"Purchase {sub.subscription_type}",
                tracking_number=str(sub.tracking_number),
            )

        except ValueError as e:
            self.member.wallet_balance += price
            if self.user_service:
                self.user_service.save()   
            print(f"Error: {e}")

    def show_transactions(self):
        if self.wallet_service is None:
            print("Wallet service not available.")
            return

        try:
            transactions = self.wallet_service.get_transactions(self.member.id)
        except Exception as e:
            print(f"Error: {e}")
            return

        if not transactions:
            print("You do not have any transactions.")
            return

        print(f"\n--- My Transactions ({len(transactions)}) ---")
        print(f"{'Date':<18} {'Type':<10} {'Amount':<12} {'Tracking':<12} Description")
        print("-" * 75)

        for t in transactions:
            date_str = t.date.strftime("%Y-%m-%d %H:%M")
            print(f"{date_str:<18} {t.transaction_type:<10} "
                  f"{t.amount:<12} {t.tracking_number:<12} {t.description}")


    def show_workout_plan(self):
        if self.workout_service is None:
            print("Workout service not available.")
            return

        try:
            workouts = self.workout_service.get_workouts_by_member(self.member.id)
        except Exception as e:
            print(f"Error: {e}")
            return

        if not workouts:
            print("You don't have any workout plan.")
            return

        for w in workouts:
            print(f"\n--- Workout ID: {w.id} | Class ID: {w.class_id} | Coach ID: {w.coach_id} ---")
            if not w.exercises:
                print("  (No exercises yet)")
                continue
            for i, ex in enumerate(w.exercises, 1):
                print(f"  [{i}] {ex.name}")
                print(f"      Sets: {ex.sets} | Reps: {ex.reps} | Rest: {ex.rest_time}s")
                print(f"      {ex.description or '-'}")

