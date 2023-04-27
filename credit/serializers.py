from credit.models import Account, Agreement, Card, Credit, CreditOrder, PaymentSchedule, Product
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "principal_debt", "interest_debt")


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ("number", "agreement_date", "termination_date")


class CreditSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(source="order.product.name", read_only=True)
    principal_debt = AccountSerializer(source="account_credit", many=True, read_only=True)
    termination_date = AgreementSerializer(source="agreement_credit", many=True, read_only=True)

    class Meta:
        model = Credit

        fields = (
            "id",
            "name",
            "principal_debt",
            "credit_limit",
            "currency_code",
            "termination_date",
        )


class CreditOrderSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    amount = serializers.DecimalField(max_digits=23, decimal_places=4, read_only=True)

    class Meta:
        model = CreditOrder
        fields = (
            "id",
            "product_id",
            "product_name",
            "status",
            "amount",
            "period_months",
            "creation_date",
        )


class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = ("payment_date", "principal", "interest")


class AccountPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "account_number",
            "principal_debt",
            "interest_debt",
        )


class AgreementIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ("id",)


class CreditPaymentScheduleSerializer(serializers.ModelSerializer):
    account = AccountPaymentSerializer(source="account_credit", many=True, read_only=True)
    agreement_id = AgreementIdSerializer(source="agreement_credit", many=True, read_only=True)
    payments = PaymentScheduleSerializer(source="schedule_credit", many=True, read_only=True)

    class Meta:
        model = Credit
        fields = ("agreement_id", "account", "payments")


class CreditOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditOrder
        fields = (
            "product",
            "amount",
            "period_months",
            "creation_date",
            "monthly_income",
            "monthly_expenditure",
            "employer_identification_number",
        )


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("card_number", "status", "transaction_limit")


class PinCodeSerializer(serializers.ModelSerializer):
    def validate(self, data):
        pin = data["pin"]
        if not pin.isnumeric() or len(pin) != 4:
            raise serializers.ValidationError("Pin must be digit with 4 symbols")
        return data

    class Meta:
        model = Card
        fields = ("card_number", "pin")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CardNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("card_number",)


class CreditAgreementSerializer(serializers.ModelSerializer):
    agreement = AgreementIdSerializer(source="agreement_credit", many=True, read_only=True)
    account = AccountSerializer(source="account_credit", many=True, read_only=True)
    payment_schedule = PaymentScheduleSerializer(
        source="schedule_credit", many=True, read_only=True
    )

    class Meta:
        model = Credit
        fields = ("agreement", "account", "currency_code", "payment_schedule")
