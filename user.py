import re
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

from utils.alias import to_camel


class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(pattern=r'^\d{5}$')

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class User(BaseModel):
    id: str
    email: EmailStr
    age: int = Field(ge=18, le=120)
    address: Address
    social_security_number: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        pattern = r"^ACC-\d{4}$"
        try:
            UUID(v)
            return v
        except ValueError:
            if not re.match(pattern, v):
                raise ValueError("ID must be UUID or format ACC-XXXX")
        return v

    def model_dump_safe(self):
        return self.model_dump(exclude={"social_security_number"})
