import zoneinfo

import pytest
from credit.models import Card
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Factory
from microservice_credit import settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tests import factories


class TestCard(APITestCase):
    """Credit card test"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("test", "test@test.ru", "test")
        self.account = factories.Account()
        self.fake = Factory.create()
        self.card_obj = Card.objects.create(
            card_number=self.fake.bothify(text="1234567891234567"),
            account_id=self.account.id,
            holder_name=self.fake.name(),
            expiration_date=self.fake.date_time(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE)),
            payment_system=self.fake.random_element(elements=("RUB", "USD", "EUR")),
            balance=self.fake.random_int(min=0, max=999999999999999999),
            status=self.fake.bothify(text="BLOCKED"),
            transaction_limit=self.fake.random_int(min=0, max=999999999999999999),
            delivery_point=self.fake.bothify(text="####################"),
            is_digital_wallet=self.fake.random_element(elements=(True, False)),
            is_virtual=self.fake.random_element(elements=(True, False)),
            co_brand=self.fake.bothify(text="####################"),
            pin=self.fake.bothify(text="0000"),
        )
        self.client.force_authenticate(user=self.user)
        self.url_status = reverse("credit:change-status-card")
        self.url_pin = reverse("credit:change-pin")

    @pytest.mark.django_db
    def test_change_card_status_correctly(self):
        response = self.client.patch(
            path=self.url_status,
            data={
                "card_number": self.card_obj.card_number,
                "status": "ACTIVE",
                "transaction_limit": self.card_obj.transaction_limit,
            },
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_change_card_same_status(self):
        response = self.client.patch(
            path=self.url_status,
            data={
                "card_number": self.card_obj.card_number,
                "status": "BLOCKED",
                "transaction_limit": self.card_obj.transaction_limit,
            },
        )
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.django_db
    def test_change_card_incorrect_status(self):
        response = self.client.patch(
            path=self.url_status,
            data={
                "card_number": self.card_obj.card_number,
                "status": "EXPIRED",
                "transaction_limit": self.card_obj.transaction_limit,
            },
        )
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.django_db
    def test_change_card_status_incorrect_card_number(self):
        response = self.client.patch(
            path=self.url_status,
            data={"card_number": self.card_obj.card_number, "status": "ACTIVE"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_change_pin(self):
        response = self.client.post(
            path=self.url_pin, data={"card_number": self.card_obj.card_number, "pin": "1111"}
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_change_incorrectly_pin(self):
        response = self.client.post(
            path=self.url_pin, data={"card_number": self.card_obj.card_number, "pin": "some"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_change_same_pin(self):
        response = self.client.post(
            path=self.url_pin, data={"card_number": self.card_obj.card_number, "pin": "0000"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_change_incorrect_number(self):
        response = self.client.post(path=self.url_pin, data={"card_number": 0, "pin": "0000"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.usefixtures("create_card", "client")
class TestCards:
    @pytest.mark.django_db
    def test_close_card(self, create_card, client):
        close_card_url = reverse("credit:close_card")
        res = client.delete(f"{close_card_url}?cardId={create_card.id}")
        assert res.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_set_card_limit(self, create_card, client):
        close_card_url = reverse("credit:set_card_limit")
        res = client.patch(
            path=close_card_url,
            data={"card_number": create_card.card_number, "transaction_limit": "12000.0000"},
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.data["transaction_limit"] == "12000.0000"
