import csv
import os
import time


def clear_screen(wait=False):
    if wait:
        time.sleep(3)

    # try to clear the screen on different systems
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class CurrencyConverter:
    def __init__(self):
        self.base_currency = "GBP"
        self.fallback_rates = {
            "EUR": 1.17,
            "USD": 1.27,
            "TRY": 41.30,
            "JPY": 190.00,
        }
        self.rates = {}

    def fetch_rates(self):
        url = "https://api.exchangerate.host/latest"
        params = {"base": self.base_currency}

        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            raw = data.get("rates")

            if not raw:
                # if the API gave something odd, pretend it failed
                raise Exception("no rates in response")

            # store keys in upper case
            self.rates = {code.upper(): value for code, value in raw.items()}

            # make sure our main currencies always exist
            for code, value in self.fallback_rates.items():
                if code not in self.rates:
                    self.rates[code] = value

            print("Live exchange rates loaded.")
        except Exception:
            # if anything goes wrong, just use the fallback completely
            self.rates = dict(self.fallback_rates)
            print("Could not load live rates, using fallback values instead.")

    def convert(self, amount_gbp, target_currency):
        if not self.rates:
            self.fetch_rates()

        code = target_currency.strip().upper()
        rate = self.rates.get(code)

        if rate is None:
            print("Currency not supported.")
            clear_screen(wait=True)
            return None, code

        return amount_gbp * rate, code

    def menu(self):
        clear_screen()
        print("\nCurrency converter")
        print("Examples of codes: EUR, USD, TRY, JPY")

        try:
            amount_gbp = float(input("Enter amount in GBP: "))
        except ValueError:
            print("That is not a valid number.")
            clear_screen(wait=True)
            return

        target = input("Enter target currency code: ")
        result, code = self.convert(amount_gbp, target)

        if result is not None:
            print(f"{amount_gbp:.2f} GBP is about {result:.2f} {code}")
            input("Press Enter to go back to the main menu...")
            clear_screen()


class BudgetTracker:
    def __init__(self):
        self.budget = 0.0
        self.spent = 0.0
        self.expenses = []

    def menu(self):
        clear_screen()
        print("\nBudget tracker")

        try:
            self.budget = float(input("Total trip budget in GBP: "))
        except ValueError:
            print("That is not a valid number.")
            clear_screen(wait=True)
            return

        self.spent = 0.0
        self.expenses = []

        print("Enter each expense, type q when you are done.\n")

        while True:
            name = input("Expense name (or q to finish): ").strip()
            name = name.title()
            if name.lower() == "q":
                break

            if name == "":
                print("Expense name cannot be empty.")
                clear_screen(wait=True)
                continue

            try:
                amount = float(input("Amount in GBP: "))
            except ValueError:
                print("That is not a valid number.")
                clear_screen(wait=True)
                continue

            self.spent += amount
            self.expenses.append((name, amount))

            remaining = self.budget - self.spent
            print(f"Added {amount:.2f} for {name}. Remaining: {remaining:.2f} GBP")
            if remaining < 0:
                print("Warning, you are over budget.")

        self.show_summary()
        input("Press Enter to go back to the main menu...")
        clear_screen()

    def show_summary(self):
        print("\nTrip summary")
        print(f"Budget:    {self.budget:.2f} GBP")
        print(f"Spent:     {self.spent:.2f} GBP")
        print(f"Remaining: {self.budget - self.spent:.2f} GBP")

        if self.expenses:
            max_item = self.expenses[0]
            for item in self.expenses[1:]:
                if item[1] > max_item[1]:
                    max_item = item
            print(f"Largest expense: {max_item[0]} at {max_item[1]:.2f} GBP")
        else:
            print("No expenses recorded.")


class PackingList:
    def __init__(self, filename="packing_list.csv"):
        self.filename = filename
        self.items = []
        self.load_from_csv()

    def load_from_csv(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r", newline="", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item_name = row.get("item", "").strip()
                packed_value = row.get("packed", "False").strip().lower()
                if item_name:
                    self.items.append({
                        "item": item_name,
                        "packed": packed_value == "true"
                    })

    def save_to_csv(self):
        with open(self.filename, "w", newline="", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=["item", "packed"])
            writer.writeheader()
            for entry in self.items:
                writer.writerow({
                    "item": entry["item"],
                    "packed": str(entry["packed"])
                })

    def show_items(self):
        if not self.items:
            print("Your packing list is empty.")
            return

        print("Packing list:")
        for i, entry in enumerate(self.items, start=1):
            status = "Yes" if entry["packed"] else "No"
            print(f"{i}. {entry['item']} (packed: {status})")

    def add_item(self):
        name = input("Item to add: ").strip()
        name = name.title()
        if name:
            self.items.append({"item": name, "packed": False})
            self.save_to_csv()
            print(f"Added {name}.")
            time.sleep(2)

    def toggle_packed(self):
        if not self.items:
            print("List is empty.")
            clear_screen(wait=True)
            return

        # show items so you know which number to pick
        clear_screen()
        self.show_items()

        try:
            number = int(input("Item number to toggle: "))
        except ValueError:
            print("Please enter a number.")
            clear_screen(wait=True)
            return

        if 1 <= number <= len(self.items):
            entry = self.items[number - 1]
            entry["packed"] = not entry["packed"]
            self.save_to_csv()
            print("Updated item.")
        else:
            print("Number is out of range.")
            clear_screen(wait=True)

    def remove_item(self):
        if not self.items:
            print("List is empty.")
            clear_screen(wait=True)
            return

        # show items so you know which number to pick
        print("\n")
        self.show_items()

        try:
            number = int(input("Item number to remove: "))
        except ValueError:
            print("Please enter a number.")
            clear_screen(wait=True)
            return

        if 1 <= number <= len(self.items):
            removed = self.items.pop(number - 1)
            self.save_to_csv()
            print(f"Removed {removed['item']}.")
        else:
            print("Number is out of range.")
            clear_screen(wait=True)

    def menu(self):
        while True:
            clear_screen()
            print("\nPacking checklist")
            print("1. View items")
            print("2. Add item")
            print("3. Mark or unmark packed")
            print("4. Remove item")
            print("5. Back to main menu")

            choice = input("Choose an option: ").strip().lower()

            if choice == "1":
                clear_screen()
                self.show_items()
                input("Press Enter to continue...")
            elif choice == "2":
                self.add_item()
            elif choice == "3":
                self.toggle_packed()
            elif choice == "4":
                self.remove_item()
            elif choice == "5":
                clear_screen()
                break
            else:
                print("Invalid option.")
                clear_screen(wait=True)


class TravelHelperApp:
    def __init__(self):
        self.converter = CurrencyConverter()
        self.budget = BudgetTracker()
        self.packing = PackingList()

    def main_menu(self):
        while True:
            clear_screen()
            print("Travel helper menu")
            print("1. Currency converter")
            print("2. Budget tracker")
            print("3. Packing checklist")
            print("4. Exit")

            choice = input("Choose an option: ").strip().lower()

            if choice == "1":
                self.converter.menu()
            elif choice == "2":
                self.budget.menu()
            elif choice == "3":
                self.packing.menu()
            elif choice == "4":
                clear_screen()
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
                clear_screen(wait=True)


TravelHelperApp().main_menu()





