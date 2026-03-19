import pytest
from decimal import Decimal
from datetime import date
from pydantic import ValidationError

from models.user import User
from models.transaction import Transaction
from models.insurance import InsurancePolicy
from models.account import Account
from utils.error_parser import parse_errors

def test_user_valid():
    user = User(
        id="ACC-1234",
        email="test@example.com",
        age=30,
        address={
            "street": "Main",
            "city": "NY",
            "zipCode": "12345"
        },
        socialSecurityNumber="123-45-6789"
    )
    assert user.age == 30


def test_user_invalid_age():
    with pytest.raises(Exception):
        User(
            id="ACC-1234",
            email="test@example.com",
            age=10,
            address={"street": "Main", "city": "NY", "zipCode": "12345"},
            socialSecurityNumber="123"
        )


def test_user_ssn_excluded():
    user = User(
        id="ACC-1234",
        email="test@example.com",
        age=30,
        address={"street": "Main", "city": "NY", "zipCode": "12345"},
        socialSecurityNumber="123-45-6789"
    )
    data = user.model_dump_safe()
    assert "social_security_number" not in data

def test_transaction_valid():
    tx = Transaction(
        currency="USD",
        amount="100.50",
        timestamp="2025-01-01T10:00:00",
        transactionType="CREDIT"
    )
    assert tx.amount == Decimal("100.50")


def test_transaction_invalid_currency():
    with pytest.raises(Exception):
        Transaction(
            currency="PLN",
            amount="100",
            timestamp="2025-01-01T10:00:00",
            transactionType="CREDIT"
        )


def test_transaction_negative_amount():
    with pytest.raises(Exception):
        Transaction(
            currency="USD",
            amount="-10",
            timestamp="2025-01-01T10:00:00",
            transactionType="DEBIT"
        )

def test_policy_valid():
    policy = InsurancePolicy(
        policyNumber="ABCDEFGHIJ",
        startDate=date(2025, 1, 1),
        endDate=date(2025, 2, 5),
        status="ACTIVE"
    )
    assert policy.status == "ACTIVE"


def test_policy_invalid_dates():
    with pytest.raises(Exception):
        InsurancePolicy(
            policyNumber="ABCDEFGHIJ",
            startDate=date(2025, 1, 1),
            endDate=date(2025, 1, 10),
            status="ACTIVE"
        )

def test_account_total():
    account = Account(
        user={
            "id": "ACC-1234",
            "email": "test@example.com",
            "age": 30,
            "address": {
                "street": "Main",
                "city": "NY",
                "zipCode": "12345"
            },
            "socialSecurityNumber": "123"
        },
        transactions=[
            {
                "currency": "USD",
                "amount": "100",
                "timestamp": "2025-01-01T10:00:00",
                "transactionType": "CREDIT"
            },
            {
                "currency": "USD",
                "amount": "50",
                "timestamp": "2025-01-02T10:00:00",
                "transactionType": "DEBIT"
            }
        ]
    )

    assert account.total_portfolio_value == 150

def test_account_risk_score():
    account = Account(
        user={
            "id": "ACC-1234",
            "email": "test@example.com",
            "age": 20,
            "address": {
                "street": "Main",
                "city": "NY",
                "zipCode": "12345"
            },
            "socialSecurityNumber": "123"
        },
        transactions=[
            {
                "currency": "USD",
                "amount": "100",
                "timestamp": "2025-01-01T10:00:00",
                "transactionType": "CREDIT"
            }
        ]
    )

    assert account.risk_score == "High"

def test_error_parser():
    try:
        Transaction(
            currency="BAD",
            amount="-10",
            timestamp="wrong",
            transactionType="INVALID"
        )
    except ValidationError as e:
        errors = parse_errors(e)

        assert isinstance(errors, list)
        assert "loc" in errors[0]
        assert "msg" in errors[0]
