import pytest
from credit.models import Credit
from django.urls import NoReverseMatch, reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tests import factories


class TestCredit(APITestCase):
    """Credit tests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.faker = Factory.create()

    @pytest.mark.django_db
    def test_credit_list_get_valid_address(self):
        assert len(Credit.objects.all()) == 0
        Credit.objects.create(
            order_id=factories.CreditOrder().id,
            credit_limit="12345.0000",
            currency_code="RUB",
            interest_rate="3952697469086364448.0000",
            personal_guarantees=True,
            grace_period_months=5,
            status="test_data",
            late_payment_rate=525,
        )
        assert len(Credit.objects.all()) == 1
        response = self.client.get(path=reverse("credit:credits"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0].get("credit_limit") == "12345.0000"

    @pytest.mark.django_db
    def test_credit_list_get_invalid_address(self):
        with pytest.raises(NoReverseMatch) as err:
            url_name = "not_a_valid_name"
            self.client.get(path=reverse(f"credit:{url_name}"))
        assert (
            err.value.args[0]
            == f"Reverse for '{url_name}' not found. '{url_name}' is not a valid view "
            "function or pattern name."
        )

    @pytest.mark.django_db
    def test_get_a_credit_info(self):
        credit = factories.Credit()
        assert len(Credit.objects.all()) == 1
        credit_id = credit.id
        credit_limit = credit.credit_limit
        url = reverse("credit:get_the_credit_info", kwargs={"creditId": credit_id})
        res = self.client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert int(res.data["id"]) == credit_id
        assert res.data["credit_limit"].split(".")[0] == str(credit_limit)

    @pytest.mark.django_db
    def test_product_info(self):
        product = factories.Product()
        product.is_active = True
        product.save()
        product_id = product.id
        product_info_url = reverse("credit:credit_product_info", kwargs={"productId": product_id})
        res = self.client.get(product_info_url)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["id"] == product_id
