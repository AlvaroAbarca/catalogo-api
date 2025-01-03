from django.contrib.auth.models import User
from django.db import models

from store.models import Product
from utils.models import BaseModel

# Create your models here.

class Order(BaseModel):
    order_number = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=100)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name_plural = 'Orders'

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = 'Order Items'
