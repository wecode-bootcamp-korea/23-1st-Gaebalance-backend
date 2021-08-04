from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    gender       = models.BooleanField()
    birth_date   = models.DateField()
    phone_number = models.CharField(max_length=50, unique=True)
    email        = models.CharField(max_length=200, unique=True)
    password     = models.CharField(max_length=200)
    address      = models.CharField(max_length=200)
    size         = models.ForeignKey('products.Size', on_delete=models.SET_NULL, null=True)
    color        = models.ManyToManyField('products.Color', through='UserColor', related_name='users')

    class Meta:
        db_table = 'users'

class UserColor(models.Model):
    user  = models.ForeignKey('User', on_delete=models.CASCADE)
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'users_colors'
