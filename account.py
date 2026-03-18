from typing import List
from decimal import Decimal
from pydantic import BaseModel, computed_field

from models.transaction import Transaction
from models.user import User


class Account(BaseModel):
    user: User
    transactions: List[Transaction]

    @computed_field
    @property
    def total_portfolio_value(self) -> Decimal:
        return sum(t.amount for t in self.transactions)

    @computed_field
    @property
    def risk_score(self) -> str:
        total = self.total_portfolio_value
        age = self.user.age

        if total > 10000 or age < 25:
            return "High"
        elif total > 5000:
            return "Medium"
        return "Low"
