from django.db import models

class Review(models.Model):
	user            = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
	product         = models.ForeignKey('products.Product', on_delete=models.CASCADE)
	size_rating     = models.IntegerField()
	color_rating    = models.IntegerField()
	delivery_rating = models.IntegerField()
	comment         = models.CharField(max_length=2000, null=True)
	title           = models.CharField(max_length=45)
	created_at      = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		db_table = 'reviews'

class ReviewImage(models.Model):
	review    = models.ForeignKey('Review', on_delete=models.CASCADE)
	image_url = models.CharField(max_length=2000)

	class Meta:
		db_table = 'reviews_images'

class Like(models.Model):
	user   = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
	review = models.ForeignKey('Review', on_delete=models.CASCADE)
	like   = models.BooleanField(default=False)
	
	class Meta:
		db_table = 'likes'