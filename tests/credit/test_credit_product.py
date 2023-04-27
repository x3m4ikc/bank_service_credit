import pytest
from credit.models import Product
from rest_framework import status
from tests import factories


@pytest.mark.usefixtures("auth_user", "client", "card_product_data", "credit_product_url")
class TestCreditProduct:
    """Credit product test"""

    @pytest.mark.django_db
    def test_credit_product_get_request_auth_user(
        self, auth_user, client, card_product_data, credit_product_url
    ):
        client.force_authenticate(user=auth_user)
        Product.objects.create(**card_product_data)
        for i in range(5):
            factories.Product()
        response = client.get(path=credit_product_url)
        assert len(Product.objects.all()) == 6
        assert response.data[0].get("min_sum") == "12345.0000"
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_credit_product_get_request_not_auth_user(self, client, credit_product_url):
        client.force_authenticate(user=None)
        response = client.get(path=credit_product_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
