import pytest
from credit.models import Card
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Factory
from rest_framework.test import APIClient
from tests import factories


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def fake():
    return Factory.create()


@pytest.fixture
def auth_user():
    return User.objects.create_user("test", "test@test.ru", "test")


@pytest.fixture
def credit_data(fake):
    data = {
        "order_id": 1,
        "credit_limit": "12345.0000",
        "currency_code": fake.random_element(elements=("RUB", "USD", "EUR")),
        "interest_rate": fake.random_int(min=0, max=999999999999999999),
        "personal_guarantees": True,
        "grace_period_months": fake.random_int(min=0, max=12),
        "status": "test_data",
        "late_payment_rate": fake.random_int(min=0, max=99999),
    }
    return data


@pytest.fixture
def card_product_data(fake):
    data = {
        "name": fake.text(max_nb_chars=30),
        "min_sum": "12345.0000",
        "max_sum": fake.random_int(min=0, max=999999999999999999),
        "currency_code": fake.random_element(elements=("RUB", "USD", "EUR")),
        "min_interest_rate": fake.random_int(min=0, max=99999),
        "max_interest_rate": fake.random_int(min=0, max=99999),
        "need_guarantees": fake.boolean(chance_of_getting_true=50),
        "delivery_in_cash": fake.boolean(chance_of_getting_true=50),
        "early_repayment": fake.boolean(chance_of_getting_true=50),
        "need_income_details": fake.boolean(chance_of_getting_true=50),
        "min_period_months": fake.random_int(min=0, max=12),
        "max_period_months": fake.random_int(min=0, max=12),
        "is_active": True,
        "details": fake.text(),
        "calculation_mode": fake.random_element(elements=("DIFFERENTIATED", "ANNUITY")),
        "grace_period_months": fake.random_int(min=0, max=99999),
        "rate_is_adjustable": fake.boolean(chance_of_getting_true=50),
        "rate_base": fake.text(max_nb_chars=15),
        "rate_fix_part": fake.random_int(min=0, max=99999),
        "increased_rate": fake.random_int(min=0, max=99999),
    }
    return data


@pytest.fixture
def account_credit_data(fake):
    data = {
        "credit_id": 1,
        "account_number": fake.random_int(min=0, max=999999999999999999),
        "principal_debt": fake.random_int(min=0, max=999999999999999999),
        "interest_debt": fake.random_int(min=0, max=999999999999999999),
        "is_active": "False",
        "opening_date": "2007-03-16",
        "closing_date": "2023-03-02",
        "currency_code": fake.random_element(elements=("RUB", "USD", "EUR")),
        "outstanding_principal": "1",
        "outstanding_interest_debt": "1",
    }
    return data


@pytest.fixture
def agreement_credit_data(fake):
    data = {
        "credit_id": 1,
        "number": fake.random_int(min=0, max=999999999999999999),
        "agreement_date": "2007-03-16",
        "termination_date": "2023-03-02",
        "responsible_specialist_id": fake.random_int(min=0, max=999999999999999999),
        "is_active": "False",
    }
    return data


@pytest.fixture
def payment_schedule_credit_data(fake):
    data = {
        "credit_id": 1,
        "payment_date": "2008-07-02",
        "principal": fake.random_int(min=0, max=999999999999999999),
        "interest": fake.random_int(min=0, max=999999999999999999),
    }
    return data


@pytest.fixture
def create_card():
    factory = Factory.create()
    account = factories.Account()

    card = Card.objects.create(
        card_number=factory.bothify(text="################"),
        account=account,
        holder_name=factory.bothify(text="??????????????????"),
        expiration_date=factory.date(),
        payment_system=factory.random_element(elements=("VISA", "MASTERCARD", "MIR")),
        balance=factory.bothify(text="#####"),
        status=factory.random_element(elements=("BLOCKED", "ACTIVE", "EXPIRED")),
        transaction_limit=factory.bothify(text="12345.0000"),
        delivery_point=factory.bothify(text="???????????????"),
        is_digital_wallet=False,
        is_virtual=False,
        co_brand=factory.bothify(text="???????????"),
    )
    return card


@pytest.fixture
def credit_product_url():
    return reverse("credit:credit-products")
