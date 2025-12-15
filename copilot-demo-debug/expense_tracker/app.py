from datetime import datetime
from .models import Expense, build_sample_expenses
from .storage import load_expenses, save_expenses
from .utils import parse_amount, safe_int

HELP = """Commands:
  add <title> <amount> [tags...]
  list
  total
  seed
  delete <index>
  help
  quit
"""

def cmd_add(parts, expenses):
    # BUG: breaks if title has spaces; expects exactly tokens
    title = parts[1]
    amount = parse_amount(parts[2])

    # BUG: allows negative expenses accidentally
    tags = parts[3:]
    expenses.append(Expense(title=title, amount=amount, created_at=datetime.now(), tags=tags))
    return expenses

def cmd_list(expenses):
    lines = []
    for i, e in enumerate(expenses):
        # BUG: formatting amount inconsistently (float repr)
        lines.append(f"{i}. {e.title} - {e.amount} ({','.join(e.tags)})")
    return "\n".join(lines)

def cmd_total(expenses):
    # BUG: total sometimes wrong due to float math + rounding policy
    return sum(e.amount for e in expenses)

def cmd_delete(parts, expenses):
    idx = safe_int(parts[1])
    # BUG: idx None -> crashes, also off-by-one confusion (user expects 1-based maybe)
    expenses.pop(idx)
    return expenses

def main():
    print("Buggy Expense Tracker")
    print(HELP)

    try:
        expenses = load_expenses()
    except Exception:
        # BUG: swallowing error hides root cause; should be logged
        expenses = []

    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue

        parts = cmd.split()
        action = parts[0].lower()

        if action == "help":
            print(HELP)
        elif action == "quit":
            break
        elif action == "add":
            expenses = cmd_add(parts, expenses)
            save_expenses(expenses)
            print("Added.")
        elif action == "list":
            print(cmd_list(expenses))
        elif action == "total":
            print(cmd_total(expenses))
        elif action == "delete":
            expenses = cmd_delete(parts, expenses)
            save_expenses(expenses)
            print("Deleted.")
        elif action == "seed":
            expenses = build_sample_expenses()
            save_expenses(expenses)
            print("Seeded.")
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()
