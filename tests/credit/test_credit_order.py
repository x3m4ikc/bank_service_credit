import pytest
from credit.models import CreditOrder
from credit.serializers import CreditOrderCreateSerializer
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tests import factories


class TestCreditOrder(APITestCase):
    """Credit order tests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.product = factories.Product()
        self.credit_order = CreditOrder.objects.filter(product_id=self.product.id)
        self.fake = Factory.create()
        self.user = User.objects.create_user("test", "test@test.ru", "test")
        self.amount = "12345.0000"
        self.data = {
            "product": self.product.id,
            "amount": self.fake.bothify(text=self.amount),
            "period_months": self.fake.random_int(min=1, max=12),
            "monthly_income": self.fake.random_int(min=0, max=9999999999999999999),
            "monthly_expenditure": self.fake.random_int(min=0, max=9999999999999999999),
            "employer_identification_number": self.fake.bothify(text="##########"),
        }
        self.invalid_digit = "9" * 24
        self.invalid_text = "*" * 24
        self.invalid_data = [
            (
                "product",
                self.invalid_digit,
                'Invalid Pk "999999999999999999999999" - Object Does Not Exist.',
            ),
            (
                "amount",
                self.invalid_digit,
                "Ensure That There Are No More Than 23 Digits In Total.",
            ),
            (
                "period_months",
                self.invalid_digit,
                "Ensure This Value Is Less Than Or Equal To 2147483647.",
            ),
            ("period_months", self.invalid_text, "A Valid Integer Is Required."),
            (
                "monthly_income",
                self.invalid_digit,
                "Ensure That There Are No More Than 23 Digits In Total.",
            ),
            ("monthly_income", self.invalid_text, "A Valid Number Is Required."),
            (
                "monthly_expenditure",
                self.invalid_digit,
                "Ensure That There Are No More Than 23 Digits In Total.",
            ),
            ("monthly_expenditure", self.invalid_text, "A Valid Number Is Required."),
            (
                "employer_identification_number",
                self.invalid_digit,
                "Ensure This Field Has No More Than 10 Characters.",
            ),
            (
                "employer_identification_number",
                self.invalid_text,
                "Ensure This Field Has No More Than 10 Characters.",
            ),
        ]
        assert len(CreditOrder.objects.all()) == 1

    @pytest.mark.django_db
    def test_credit_order_list_valid_data_get(self):
        CreditOrder.objects.create(
            number=self.fake.bothify(text="####################"),
            product_id=self.product.id,
            status=self.fake.random_element(elements=("PENDING", "REJECT", "APPROVED")),
            amount=self.fake.bothify(text=self.amount),
            period_months=self.fake.random_int(min=1, max=12),
            monthly_income=self.fake.random_int(min=0, max=9999999999999999999),
            monthly_expenditure=self.fake.random_int(min=0, max=9999999999999999999),
            employer_identification_number=self.fake.bothify(text="##########"),
        )
        assert len(CreditOrder.objects.all()) == 2
        response = self.client.get(path=reverse("credit:credit-orders"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data[1].get("amount") == self.amount

    @pytest.mark.django_db
    def test_credit_order_create_request_auth_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(path=reverse("credit:credit-orders-create"), data=self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("amount") == "12345.0000"
        assert response.request.get("PATH_INFO") == reverse("credit:credit-orders-create")
        assert response.request.get("REQUEST_METHOD") == "POST"
        assert len(CreditOrder.objects.all()) == 2

    @pytest.mark.django_db
    def test_credit_order_create_request_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(path=reverse("credit:credit-orders-create"), data=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_credit_order_create_bad_request_auth_user(self):
        self.client.force_authenticate(user=self.user)
        for key, invalid_value, _ in self.invalid_data:
            correct_value, self.data[key] = self.data[key], invalid_value
            response = self.client.post(path=reverse("credit:credit-orders-create"), data=self.data)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            self.data[key] = correct_value

    @pytest.mark.django_db
    def test_credit_order_serializer_valid_data(self):
        serializer = CreditOrderCreateSerializer(data=self.data)
        assert serializer.is_valid()
        assert serializer.data.get("amount") == self.amount
        assert dict(serializer.validated_data).keys() == self.data.keys()
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_credit_order_serializer_invalid_data(self):
        for key, invalid_value, error_message in self.invalid_data:
            correct_value, self.data[key] = self.data[key], invalid_value
            serializer = CreditOrderCreateSerializer(data=self.data)
            assert not serializer.is_valid()
            for k, v in serializer.errors.items():
                assert v[0].title() == error_message
            self.data[key] = correct_value

    @pytest.mark.django_db
    def test_cancel_credit_order(self):
        credit_order = CreditOrder.objects.create(
            number=self.fake.bothify(text="####################"),
            product_id=self.product.id,
            status=self.fake.random_element(elements=("PENDING",)),
            amount=self.fake.bothify(text="12345.0000"),
            period_months=self.fake.random_int(min=1, max=12),
            monthly_income=self.fake.random_int(min=0, max=9999999999999999999),
            monthly_expenditure=self.fake.random_int(min=0, max=9999999999999999999),
            employer_identification_number=self.fake.bothify(text="##########"),
        )
        credit_url = reverse("credit:cancel_credit_order", kwargs={"pk": credit_order.id})
        res = self.client.delete(credit_url)
        assert res.status_code == status.HTTP_204_NO_CONTENT
