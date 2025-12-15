from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class Expense:
    title: str
    amount: float
    created_at: datetime
    tags: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Expense":
        # BUG: assumes created_at is always ISO string; breaks if it's already datetime or missing
        created = datetime.fromisoformat(d["created_at"])
        return Expense(
            title=d["title"],
            amount=float(d["amount"]),
            created_at=created,
            tags=d.get("tags", []),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
        }

# BUG: mutable default arg (shared list across calls)
def build_sample_expenses(seed: List[Expense] = []):
    seed.append(
        Expense(title="Coffee", amount=3.5, created_at=datetime.now(), tags=["food"])
    )
    return seed
