from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    category     = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.CharField(max_length=45)

    class Meta:
        db_table = 'sub_categories'

class Product(models.Model):
    sub_category     = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    color            = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True, related_name='products')
    name             = models.CharField(max_length=45)
    price            = models.DecimalField(max_digits=10, decimal_places=2)
    style_code       = models.CharField(max_length=45)
    origin           = models.CharField(max_length=45)
    manufacture_date = models.DateField()
    description      = models.TextField()
    image_url        = models.CharField(max_length=2000)
    group            = models.CharField(max_length=45)

    class Meta:
        db_table = 'products'

class DetailImage(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'detail_images'

class ProductOption(models.Model):
	product = models.ForeignKey('Product', on_delete = models.CASCADE)
	size	= models.ForeignKey('Size', on_delete = models.CASCADE)
	stock 	= models.PositiveIntegerField()

	class Meta :
		db_table = 'products_options'

class Size(models.Model):
	name = models.CharField(max_length=45)

	class Meta :
		db_table = 'sizes'

class Color(models.Model):
    name  = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'colors'