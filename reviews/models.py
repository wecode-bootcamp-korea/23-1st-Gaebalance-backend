from django.db import models

class Review(models.Model):
	user 		     = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
	product 	     = models.ForeignKey('products.Product', on_delete=models.CASCADE)
	size_rating   	 = models.IntegerField()
	color_rating	 = models.IntegerField()
	delivery_rating  = models.IntegerField()
	comment		     = models.TextField(null=True)
	
	class Meta:
		db_table = 'reviews'
