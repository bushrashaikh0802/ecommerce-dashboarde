from django.db import models

class Sale(models.Model):
    transaction_id = models.CharField(max_length=50)
    date = models.DateField()
    customer_id = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    product_category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    total_amount = models.FloatField()

    def __str__(self):
        return f"{self.transaction_id} - {self.product_category}"
