from django.db import models

CURRENCY_CODE_CHOICE = (
    ("RUB", "RUB"),
    ("USD", "USD"),
    ("EUR", "EUR"),
)


class Product(models.Model):
    CALCULATION_MODE_CHOICE = (
        ("DIFFERENTIATED", "DIFFERENTIATED"),
        ("ANNUITY", "ANNUITY"),
    )

    name = models.CharField(max_length=30)
    min_sum = models.DecimalField(max_digits=23, decimal_places=4)
    max_sum = models.DecimalField(max_digits=23, decimal_places=4)
    currency_code = models.CharField(max_length=3, choices=CURRENCY_CODE_CHOICE, default="USD")
    min_interest_rate = models.DecimalField(max_digits=10, decimal_places=4)
    max_interest_rate = models.DecimalField(max_digits=10, decimal_places=4)
    need_guarantees = models.BooleanField(default=False)
    delivery_in_cash = models.BooleanField(default=False)
    early_repayment = models.BooleanField(default=False)
    need_income_details = models.BooleanField(default=False)
    min_period_months = models.IntegerField()
    max_period_months = models.IntegerField()
    is_active = models.BooleanField(default=False)
    details = models.CharField(max_length=255)
    calculation_mode = models.CharField(
        max_length=30, choices=CALCULATION_MODE_CHOICE, default="DIFFERENTIATED"
    )
    grace_period_months = models.IntegerField()
    rate_is_adjustable = models.BooleanField(default=False)
    rate_base = models.CharField(max_length=20)
    rate_fix_part = models.DecimalField(max_digits=10, decimal_places=4)
    increased_rate = models.DecimalField(max_digits=10, decimal_places=4)


class Credit(models.Model):
    TYPE_CHOICE = (
        ("OVERDRAFT", "OVERDRAFT"),
        ("REAL_ESTATE", "REAL_ESTATE"),
        ("INSTALLMENT", "INSTALLMENT"),
        ("CONSUMER", "CONSUMER"),
    )

    order = models.ForeignKey("CreditOrder", on_delete=models.CASCADE, related_name="credit_order")
    credit_type = models.CharField(max_length=11, choices=TYPE_CHOICE, default="CONSUMER")
    credit_limit = models.DecimalField(max_digits=23, decimal_places=4)
    currency_code = models.CharField(max_length=3, choices=CURRENCY_CODE_CHOICE, default="USD")
    interest_rate = models.DecimalField(max_digits=23, decimal_places=4)
    personal_guarantees = models.BooleanField(default=True)
    grace_period_months = models.IntegerField()
    status = models.CharField(max_length=30)
    late_payment_rate = models.DecimalField(max_digits=10, decimal_places=4)


class Account(models.Model):
    credit = models.ForeignKey("Credit", on_delete=models.CASCADE, related_name="account_credit")
    account_number = models.CharField(max_length=30)
    principal_debt = models.DecimalField(max_digits=23, decimal_places=4)
    interest_debt = models.DecimalField(max_digits=23, decimal_places=4)
    is_active = models.BooleanField(default=False)
    opening_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField()
    currency_code = models.CharField(max_length=3, choices=CURRENCY_CODE_CHOICE, default="USD")
    outstanding_principal = models.DecimalField(max_digits=23, decimal_places=4)
    outstanding_interest_debt = models.DecimalField(max_digits=23, decimal_places=4)


class Card(models.Model):
    PAYMENT_SYSTEM_CHOICE = (
        ("VISA", "VISA"),
        ("MASTERCARD", "MASTERCARD"),
        ("MIR", "MIR"),
    )

    STATUS_CHOICE = (
        ("BLOCKED", "BLOCKED"),
        ("ACTIVE", "ACTIVE"),
        ("EXPIRED", "EXPIRED"),
    )

    card_number = models.CharField(max_length=16)
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="card_account")
    holder_name = models.CharField(max_length=50)
    expiration_date = models.DateField()
    payment_system = models.CharField(max_length=30, choices=PAYMENT_SYSTEM_CHOICE, default="VISA")
    balance = models.DecimalField(max_digits=23, decimal_places=4)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default="BLOCKED")
    transaction_limit = models.DecimalField(max_digits=23, decimal_places=4)
    delivery_point = models.CharField(max_length=30)
    is_digital_wallet = models.BooleanField(default=False)
    is_virtual = models.BooleanField(default=False)
    co_brand = models.CharField(max_length=30)
    pin = models.CharField(max_length=4, default=0000)


class Agreement(models.Model):
    credit = models.ForeignKey("Credit", on_delete=models.CASCADE, related_name="agreement_credit")
    number = models.CharField(max_length=20)
    agreement_date = models.DateField()
    termination_date = models.DateField()
    responsible_specialist_id = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)


class CreditOrder(models.Model):
    STATUS_CHOICE = (
        ("PENDING", "PENDING"),
        ("REJECT", "REJECT"),
        ("APPROVED", "APPROVED"),
    )

    number = models.CharField(max_length=20)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="oder_product")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="PENDING")
    amount = models.DecimalField(max_digits=23, decimal_places=4)
    period_months = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)
    monthly_income = models.DecimalField(max_digits=23, decimal_places=4)
    monthly_expenditure = models.DecimalField(max_digits=23, decimal_places=4)
    employer_identification_number = models.CharField(max_length=10)


class PaymentSchedule(models.Model):
    credit = models.ForeignKey("Credit", on_delete=models.CASCADE, related_name="schedule_credit")
    payment_date = models.DateField()
    principal = models.DecimalField(max_digits=23, decimal_places=4)
    interest = models.DecimalField(max_digits=23, decimal_places=4)


class Operation(models.Model):
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="operation_account"
    )
    operation_type = models.ForeignKey(
        "OperationType", on_delete=models.CASCADE, related_name="operation_type_related"
    )
    sum = models.DecimalField(max_digits=23, decimal_places=4)
    completed_at = models.DateTimeField()
    details = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=3, choices=CURRENCY_CODE_CHOICE, default="USD")


class OperationType(models.Model):
    operation_type = models.CharField(max_length=30, null=False)
    is_debit = models.BooleanField(default=False)
