from django.db import models

class Cart(models.Model):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    count   = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'
