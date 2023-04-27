from credit.views import (
    CancelCreditOrder,
    CloseCard,
    CreditAgreementDetails,
    CreditCardLimit,
    CreditListAPIView,
    CreditOrderCreateAPIView,
    CreditOrderListAPIView,
    CreditProductInfo,
    CreditProductListAPIView,
    CreditScheduleView,
    ResetPinCode,
    StatusCard,
    TheCreditInfo,
)
from django.urls import path

app_name = "credit"
urlpatterns = [
    path(
        "credits/<int:creditId>/schedule/",
        CreditScheduleView.as_view(),
        name="get_credit_payment_schedule",
    ),
    path("credits/", CreditListAPIView.as_view(), name="credits"),
    path("credits/<int:creditId>/", TheCreditInfo.as_view(), name="get_the_credit_info"),
    path("credit-orders/", CreditOrderListAPIView.as_view(), name="credit-orders"),
    path("credit-orders/new/", CreditOrderCreateAPIView.as_view(), name="credit-orders-create"),
    path("credit-cards/active-cards/", StatusCard.as_view(), name="change-status-card"),
    path("credit-cards/code", ResetPinCode.as_view(), name="change-pin"),
    path("credit-cards/", CloseCard.as_view(), name="close_card"),
    path(
        "credit-orders/<int:pk>/pending/",
        CancelCreditOrder.as_view(),
        name="cancel_credit_order",
    ),
    path(
        "credit-products/<int:productId>/", CreditProductInfo.as_view(), name="credit_product_info"
    ),
    path("credit-cards/limit/", CreditCardLimit.as_view(), name="set_card_limit"),
    path("credit-products/", CreditProductListAPIView.as_view(), name="credit-products"),
    path(
        "credits/<int:agreement_id>/details/",
        CreditAgreementDetails.as_view(),
        name="credit-agreement-details",
    ),
]
