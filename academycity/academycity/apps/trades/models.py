from django.db import models
from decimal import Decimal


class PlacedOrders(models.Model):
    Right = models.CharField(max_length=1)
    Ticker = models.CharField(max_length=10)
    OrderDate = models.DateTimeField('date ordered', auto_now_add=True)
    ContractDate = models.CharField(max_length=8)

    LeftStrike = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftOrderAskPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftOrderBidPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftOrderAveragePrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftOrderClose = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftOrderBidSize = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftOrderAskSize = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftActualPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    LeftActualUndPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))

    MidStrike = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidOrderAskPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidOrderBidPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidOrderAveragePrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidOrderClose = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidOrderBidSize = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidOrderAskSize = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidActualPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    MidActualUndPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))

    RightStrike = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightOrderAskPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightOrderBidPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightOrderAveragePrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightOrderClose = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightOrderBidSize = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightOrderAskSize = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightActualPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    RightActualUndPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))

    StrategyPrice = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    TransactionCost = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))

