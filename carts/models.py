from django.db import models

class Cart(models.Model):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('products.Size', on_delete=models.CASCADE)
    count   = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'carts'
