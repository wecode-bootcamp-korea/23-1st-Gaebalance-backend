# Generated by Django 3.2.4 on 2021-08-10 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
