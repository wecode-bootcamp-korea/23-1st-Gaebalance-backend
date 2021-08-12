import json

from django.http      import JsonResponse, request
from django.views     import View
from django.db.models import F,Avg
from reviews.models   import Review
from users.models     import User
from products.models  import Product
from users.utils      import login_decorator

class ReviewView(View):
    @login_decorator    
    def post(self,request):
        try:
            data = json.loads(request.body)

            if data["title"] == "" :
                return JsonResponse({"MESSAGE":"NULL_REVIEWS"}, status = 400)

            if data["size_rating"] == "" or data["color_rating"] == "" or data["delivery_rating"] == "" :
                return JsonResponse({"MESSAGE":"NULL_RATING"}, status = 400)

            RATING_MAX = 6

            if data["size_rating"] >= RATING_MAX or data["color_rating"] >= RATING_MAX or data["delivery_rating"] >= RATING_MAX :
                return JsonResponse({"MESSAGE":"RATING_INPUT_ERROR"}, status = 400)
            
            if not Product.objects.filter(id=data["product_id"]).exists() :
                return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXISTS"}, status = 400)

            Review.objects.create( 
                user            = request.user,
                product_id      = data["product_id"],
                size_rating     = data["size_rating"],
                color_rating    = data["color_rating"],
                delivery_rating = data["delivery_rating"],
                title           = data["title"],
                comment         = data["comment"],
            )

            return JsonResponse({"MESSAGE":"CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)    

    def get(self,request, review_id):
        reviews = Review.objects.all()
        result = [] 
 
        rating_field = Review.objects.annotate(all_rating = (F('size_rating')+ F('color_rating') + F('delivery_rating'))/3)
        all_rating = rating_field.aggregate(Avg("all_rating"))

        result = [
            {
                "user"            : review.user.id,
                "product_id"      : review.product_id ,
                "created_at"      : review.created_at,
                "size_rating"     : review.size_rating,
                "color_rating"    : review.color_rating,
                "delivery_rating" : review.delivery_rating,
                "all_rating"      : all_rating['all_rating__avg'],
                "title"           : review.title,
                "comment"         : review.comment,

            } for review in reviews]

        return JsonResponse ({"result": result}, status = 200)

    @login_decorator
    def delete (self,request,review_id):

        if not Review.objects.filter(id=review_id, user = request.user).exists():
            return JsonResponse({"MESSAGE": "NO_REVIEWS"}, status = 400)

        Review.objects.filter(id=review_id).delete()

        return JsonResponse ({"MESSAGE" : "DELETE"}, status = 204)    

    @login_decorator
    def patch (self,request, review_id):
        try:
            data = json.loads(request.body)

            if not Review.objects.filter(id=review_id, user = request.user).exists():
              return JsonResponse({"MESSAGE": "NO_REVIEWS"}, status = 400)
    
            Review.objects.filter(id=review_id).update(title= data["title"], comment= data["comment"])
            return JsonResponse ({"MESSAGE" : "UPDATE"}, status = 200)

        except KeyError: 
            return JsonResponse ({"MESSAGE":"KEY_ERROR"},status = 400)