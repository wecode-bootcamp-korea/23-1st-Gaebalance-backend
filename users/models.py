from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    gender       = models.PositiveSmallIntegerField()
    birth_date   = models.DateField()
    phone_number = models.CharField(max_length=50, unique=True)
    email        = models.CharField(max_length=200, unique=True)
    password     = models.CharField(max_length=200)
    address      = models.CharField(max_length=200)
    size         = models.ForeignKey('products.Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'

class Cart(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    count   = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'
