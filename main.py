from models.user import User
from models.transaction import Transaction
from models.account import Account
from utils.error_parser import parse_errors
from pydantic import ValidationError


raw_data = {
    "user": {
        "id": "ACC-1234",
        "email": "test@example.com",
        "age": 30,
        "address": {
            "street": "Main St",
            "city": "NY",
            "zipCode": "12345"
        },
        "socialSecurityNumber": "123-45-6789"
    },
    "transactions": [
        {
            "currency": "USD",
            "amount": "100.50",
            "timestamp": "2025-01-01T10:00:00",
            "transactionType": "CREDIT"
        }
    ]
}

try:
    account = Account(**raw_data)

    print(account.model_dump())
    print(account.user.model_dump_safe())

except ValidationError as e:
    print(parse_errors(e))
