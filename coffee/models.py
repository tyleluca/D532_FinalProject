from django.db import models

class Product(models.Model):
    productId = models.AutoField(primary_key=True, db_column='productId')
    productCategory = models.CharField(max_length=255, db_column='productCategory')
    productType = models.CharField(max_length=255, db_column='productType')
    productDetail = models.TextField(db_column='productDetail')

    class Meta:
        db_table = 'product'


class Store(models.Model):
    storeId = models.AutoField(primary_key=True, db_column='storeId')
    storeLocation = models.CharField(max_length=255, db_column='storeLocation')

    class Meta:
        db_table = 'store'


class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True, db_column='transactionId')
    transactionQty = models.IntegerField(db_column='transactionQty')
    transactionDatetime = models.DateTimeField(db_column='transactionDatetime')
    storeId = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        db_column='storeId',
        to_field='storeId'
    )
    productId = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column='productId',
        to_field='productId'
    )
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2, db_column='unitPrice')

    class Meta:
        db_table = 'transaction'
