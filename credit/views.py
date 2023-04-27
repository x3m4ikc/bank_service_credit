from credit.models import Card, Credit, CreditOrder, Product
from credit.serializers import (
    CardSerializer,
    CreditAgreementSerializer,
    CreditOrderCreateSerializer,
    CreditOrderSerializer,
    CreditPaymentScheduleSerializer,
    CreditSerializer,
    PinCodeSerializer,
    ProductSerializer,
)
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CreditScheduleView(generics.RetrieveAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditPaymentScheduleSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        credit_id = self.kwargs.get("creditId")
        try:
            credit = Credit.objects.get(id=credit_id)
            return credit
        except ObjectDoesNotExist:
            return Response("No such credit")


class CreditListAPIView(generics.ListAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer


class CreditOrderListAPIView(generics.ListAPIView):
    queryset = CreditOrder.objects.all()
    serializer_class = CreditOrderSerializer


class CreditOrderCreateAPIView(generics.CreateAPIView):
    queryset = CreditOrder.objects.all()
    serializer_class = CreditOrderCreateSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)


class TheCreditInfo(generics.RetrieveAPIView):
    serializer_class = CreditSerializer
    queryset = Credit.objects.all()

    def get_object(self):
        credit_id = self.kwargs.get("creditId")
        try:
            credit = Credit.objects.get(id=credit_id)
            return credit
        except ObjectDoesNotExist:
            return Response("No such credit")


class StatusCard(generics.UpdateAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    # permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_number = serializer.validated_data["card_number"]
        card_status = serializer.validated_data["status"]
        card = get_object_or_404(Card, card_number=card_number)
        if card.status == card_status or card_status == "EXPIRED":
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        card.status = card_status
        card.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPinCode(generics.CreateAPIView):
    serializer_class = PinCodeSerializer
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_number = serializer.validated_data["card_number"]
        pin = serializer.validated_data["pin"]
        try:
            card = Card.objects.get(card_number=card_number)
            if card.pin == pin:
                return Response("The same pin", status=status.HTTP_400_BAD_REQUEST)
            card.pin = pin
            card.save()
            return Response("Pincode is changed successfully", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("Operation invalid", status=status.HTTP_400_BAD_REQUEST)


class CancelCreditOrder(generics.DestroyAPIView):
    serializer_class = CreditOrderSerializer
    queryset = CreditOrder.objects.filter(status="PENDING")
    lookup_field = "pk"


class CloseCard(generics.DestroyAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def get_object(self):
        credit_id = self.request.GET.get("cardId")
        credit = get_object_or_404(Card, id=credit_id)
        return credit


class CreditProductInfo(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_object(self):
        product_id = self.kwargs["productId"]
        try:
            if type(product_id) is not int:
                raise ValueError
            product = Product.objects.get(id=product_id)
            return product
        except (ValueError, ObjectDoesNotExist):
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class CreditCardLimit(generics.UpdateAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_number = serializer.validated_data["card_number"]
        card_limit = serializer.validated_data["transaction_limit"]
        card = get_object_or_404(Card, card_number=card_number)
        card.transaction_limit = card_limit
        card.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreditProductListAPIView(generics.ListAPIView):
    """
    ViewSet for retrieving products as a list if many, or a single object.
    """

    queryset = Product.objects.filter(is_active="True")
    serializer_class = ProductSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)


class CreditAgreementDetails(generics.RetrieveAPIView):
    """
    Retrieve credit details by agreement_id.
    """

    queryset = Credit.objects.all()
    serializer_class = CreditAgreementSerializer

    def get_object(self):
        agreement_id = self.kwargs.get("agreement_id")
        try:
            credit = Credit.objects.filter(agreement_credit=agreement_id).first()
            return credit
        except ObjectDoesNotExist:
            return Response("No such credit")
