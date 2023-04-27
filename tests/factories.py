import zoneinfo

import factory
from credit import models
from django.db.models.signals import post_save
from factory import fuzzy
from faker import Factory
from microservice_credit import settings

Faker = Factory.create
fake = Faker()


@factory.django.mute_signals(post_save)
class Product(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: fake.text(max_nb_chars=30))
    min_sum = factory.Sequence(lambda n: fake.random_int(min=0, max=99999999))
    max_sum = factory.Sequence(lambda n: fake.random_int(min=99999999, max=9999999999))
    currency_code = fuzzy.FuzzyChoice(i[0] for i in models.CURRENCY_CODE_CHOICE)
    min_interest_rate = factory.Sequence(lambda n: fake.random_int(min=0, max=9999))
    max_interest_rate = factory.Sequence(lambda n: fake.random_int(min=9999, max=999999))
    need_guarantees = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    delivery_in_cash = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    early_repayment = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    need_income_details = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    min_period_months = factory.Sequence(lambda n: fake.random_int(min=1, max=6))
    max_period_months = factory.Sequence(lambda n: fake.random_int(min=6, max=12))
    is_active = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    details = factory.Sequence(lambda n: fake.text(max_nb_chars=255))
    calculation_mode = fuzzy.FuzzyChoice(i[0] for i in models.Product.CALCULATION_MODE_CHOICE)
    grace_period_months = factory.Sequence(lambda n: fake.random_int(min=1, max=12))
    rate_is_adjustable = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    rate_base = factory.Sequence(lambda n: fake.text(max_nb_chars=20))
    rate_fix_part = factory.Sequence(lambda n: fake.random_int(min=0, max=99999))
    increased_rate = factory.Sequence(lambda n: fake.random_int(min=0, max=99999))
    oder_product = factory.RelatedFactory(
        "tests.factories.CreditOrder", factory_related_name="product"
    )


@factory.django.mute_signals(post_save)
class CreditOrder(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CreditOrder

    number = factory.Sequence(lambda n: fake.bothify(text="####################"))
    product = factory.SubFactory(Product, oder_product=None)
    status = fuzzy.FuzzyChoice(i[0] for i in models.CreditOrder.STATUS_CHOICE)
    amount = fuzzy.FuzzyDecimal(0, 9999999999999999999, 4)
    period_months = factory.Sequence(lambda n: fake.random_int(min=1, max=12))
    creation_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    monthly_income = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    monthly_expenditure = factory.Sequence(
        lambda n: fake.random_int(min=0, max=9999999999999999999)
    )
    employer_identification_number = factory.Sequence(lambda n: fake.bothify(text="##########"))


@factory.django.mute_signals(post_save)
class Credit(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Credit

    order = factory.SubFactory(CreditOrder)
    credit_type = fuzzy.FuzzyChoice(i[0] for i in models.Credit.TYPE_CHOICE)
    credit_limit = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    currency_code = fuzzy.FuzzyChoice(i[0] for i in models.CURRENCY_CODE_CHOICE)
    interest_rate = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    personal_guarantees = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    grace_period_months = factory.Sequence(lambda n: fake.random_int(min=1, max=12))
    status = factory.Sequence(lambda n: fake.text(max_nb_chars=30))
    late_payment_rate = factory.Sequence(lambda n: fake.random_int(min=0, max=999999))
    agreement_credit = factory.RelatedFactory(
        "tests.factories.Agreement", factory_related_name="credit"
    )
    account_credit = factory.RelatedFactory(
        "tests.factories.Account", factory_related_name="credit"
    )
    schedule_credit = factory.RelatedFactory(
        "tests.factories.PaymentSchedule", factory_related_name="credit"
    )


@factory.django.mute_signals(post_save)
class Agreement(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Agreement

    credit = factory.SubFactory(Credit, agreement_credit=None)
    number = factory.Sequence(lambda n: fake.bothify(text="####################"))
    agreement_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    termination_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    responsible_specialist_id = factory.Sequence(
        lambda n: fake.bothify(text="####################")
    )
    is_active = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))


@factory.django.mute_signals(post_save)
class Account(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account

    credit = factory.SubFactory(Credit, account_credit=None)
    account_number = factory.Sequence(lambda n: fake.bothify(text="#############################"))
    principal_debt = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    interest_debt = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    is_active = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    opening_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    closing_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    currency_code = fuzzy.FuzzyChoice(i[0] for i in models.CURRENCY_CODE_CHOICE)
    outstanding_principal = factory.Sequence(
        lambda n: fake.random_int(min=0, max=9999999999999999999)
    )
    outstanding_interest_debt = factory.Sequence(
        lambda n: fake.random_int(min=0, max=9999999999999999999)
    )
    operation_account = factory.RelatedFactory(
        "tests.factories.Operation", factory_related_name="account"
    )
    card_account = factory.RelatedFactory("tests.factories.Card", factory_related_name="account")


@factory.django.mute_signals(post_save)
class PaymentSchedule(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PaymentSchedule

    credit = factory.SubFactory(Credit, schedule_credit=None)
    payment_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    principal = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    interest = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))


@factory.django.mute_signals(post_save)
class Card(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Card

    card_number = factory.Sequence(lambda n: fake.bothify(text="################"))
    account = factory.SubFactory(Account, card_account=None)
    holder_name = factory.Sequence(lambda n: fake.name())
    expiration_date = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    payment_system = fuzzy.FuzzyChoice(i[0] for i in models.Card.PAYMENT_SYSTEM_CHOICE)
    balance = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    status = fuzzy.FuzzyChoice(i[0] for i in models.Card.STATUS_CHOICE)
    transaction_limit = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    delivery_point = factory.Sequence(lambda n: fake.text(max_nb_chars=30))
    is_digital_wallet = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    is_virtual = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    co_brand = factory.Sequence(lambda n: fake.text(max_nb_chars=30))


@factory.django.mute_signals(post_save)
class OperationType(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OperationType

    operation_type = factory.Sequence(lambda n: fake.text(max_nb_chars=30))
    is_debit = factory.Sequence(lambda n: fake.boolean(chance_of_getting_true=50))
    operation_type_related = factory.RelatedFactory(
        "tests.factories.Operation", factory_related_name="operation_type"
    )


@factory.django.mute_signals(post_save)
class Operation(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Operation

    account = factory.SubFactory(Account, operation_account=None)
    operation_type = factory.SubFactory(OperationType, operation_type_related=None)
    sum = factory.Sequence(lambda n: fake.random_int(min=0, max=9999999999999999999))
    completed_at = factory.Sequence(
        lambda n: fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
    )
    details = factory.Sequence(lambda n: fake.text(max_nb_chars=255))
    currency_code = fuzzy.FuzzyChoice(i[0] for i in models.CURRENCY_CODE_CHOICE)
