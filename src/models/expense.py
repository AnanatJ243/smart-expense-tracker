from dataclasses import dataclass
from datetime import date

@dataclass
class Expense:
    expense_id: int | None
    expense_date: date
    category: str
    amount: float
    payment_mode: str
    description: str

    def to_tuple(self):
        return (self.expense_date.isoformat(), self.category, self.amount, self.payment_mode, self.description)
