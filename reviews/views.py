import json

from reviews.models        import Review
from django.http           import JsonResponse, request
from django.views          import View
from users.models          import User
from products.models       import Product
from users.utils           import login_decorator

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

            if not Product.objects.filter(id=request.product_id).exists() :
                return JsonResponse({"MESSAGE":"PRODUCT_DOES_NOT_EXISTS"}, status = 400)

            Review.objects.create( 
                user            = request.user,
                product         = data["product_id"],
                size_rating     = data["size_rating"],
                color_rating    = data["color_rating"],
                delivery_rating = data["delivery_rating"],
                title           = data["title"],
                comment         = data["comment"]
            )

            return JsonResponse({"MESSAGE":"CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)    