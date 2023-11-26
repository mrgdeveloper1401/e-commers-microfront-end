from django.db import models
from django.utils.translation import gettext_lazy as _


class StockRecord(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='stock_products')
    sku = models.CharField(max_length=64, blank=True ,null=True, unique=True)
    buy_price = models.PositiveBigIntegerField(null=True, blank=True)
    sell_price = models.PositiveBigIntegerField(null=True, blank=True)
    number_stock = models.PositiveSmallIntegerField()
    threshold_low_stack = models.PositiveSmallIntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('stock')
        verbose_name_plural = _('stocks')
        db_table = 'stock'
