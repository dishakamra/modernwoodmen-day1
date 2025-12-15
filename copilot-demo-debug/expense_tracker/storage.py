import json
from pathlib import Path
from typing import List
from .models import Expense

DEFAULT_PATH = Path("data/expenses.json")

def load_expenses(path: Path = DEFAULT_PATH) -> List[Expense]:
    # BUG: if file doesn't exist, this throws instead of returning empty list
    raw = path.read_text()  # also no encoding specified

    # BUG: if file is empty, json.loads fails
    data = json.loads(raw)

    return [Expense.from_dict(x) for x in data]

def save_expenses(expenses: List[Expense], path: Path = DEFAULT_PATH) -> None:
    # BUG: directory may not exist
    # BUG: writes invalid JSON sometimes if interrupted; no temp file strategy
    payload = [e.to_dict() for e in expenses]
    path.write_text(json.dumps(payload, indent=2))
