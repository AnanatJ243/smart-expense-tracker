from dataclasses import dataclass

@dataclass
class Budget:
    budget_id: int | None
    month: str
    category: str
    limit_amount: float
