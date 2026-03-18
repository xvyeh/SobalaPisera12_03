from datetime import date, timedelta
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ConfigDict

from utils.alias import to_camel


class PolicyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ELAPSED = "ELAPSED"
    PENDING = "PENDING"


class InsurancePolicy(BaseModel):
    policy_number: str = Field(min_length=10, max_length=10)
    start_date: date
    end_date: date
    status: PolicyStatus

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date + timedelta(days=30):
            raise ValueError("End date must be at least 30 days after start date")
        if not self.policy_number.isupper():
            raise ValueError("Policy number must be uppercase")
        return self
