import pytest
from expense_tracker.utils import parse_amount
from expense_tracker.models import build_sample_expenses
from expense_tracker.storage import save_expenses, load_expenses
from pathlib import Path

def test_parse_amount_supports_commas():
    assert parse_amount("1,000.50") == 1000.50

def test_seed_is_not_shared_across_calls():
    a = build_sample_expenses()
    b = build_sample_expenses()
    assert len(a) == 1
    assert len(b) == 1

def test_save_and_load_roundtrip(tmp_path: Path):
    p = tmp_path / "expenses.json"
    save_expenses(build_sample_expenses([]), p)
    loaded = load_expenses(p)
    assert len(loaded) == 1
    assert loaded[0].title == "Coffee"
