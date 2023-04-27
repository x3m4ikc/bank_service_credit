from django.contrib import admin

from .models import (
    Account,
    Agreement,
    Card,
    Credit,
    CreditOrder,
    Operation,
    OperationType,
    PaymentSchedule,
    Product,
)

admin.site.register(Product)
admin.site.register(Credit)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Agreement)
admin.site.register(CreditOrder)
admin.site.register(PaymentSchedule)
admin.site.register(Operation)
admin.site.register(OperationType)
