from decimal import Decimal
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

from utils.alias import to_camel


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class TransactionType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class Transaction(BaseModel):
    currency: Currency
    amount: Decimal = Field(gt=0)
    timestamp: datetime
    transaction_type: TransactionType

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @field_validator("currency")
    @classmethod
    def custom_currency_error(cls, v):
        if v not in Currency:
            raise ValueError("Please select a valid currency: USD, EUR, or GBP")
        return v
