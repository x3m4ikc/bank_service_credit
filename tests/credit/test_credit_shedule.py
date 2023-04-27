import pytest
from credit.models import Credit
from django.urls import reverse
from rest_framework import status
from tests import factories


@pytest.mark.usefixtures(
    "auth_user",
    "client",
    "credit_data",
    "account_credit_data",
    "agreement_credit_data",
    "payment_schedule_credit_data",
)
class TestCreditPaymant:
    @pytest.mark.django_db
    def test_credit_product_get_request_auth_user(
        self,
        auth_user,
        client,
    ):
        client.force_authenticate(user=auth_user)
        factories.Credit()
        response = client.get(
            path=reverse("credit:get_credit_payment_schedule", kwargs={"creditId": 1})
        )
        assert len(Credit.objects.all()) == 1
        assert response.status_code == status.HTTP_200_OK
