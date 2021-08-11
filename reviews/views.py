import json

from django.http      import JsonResponse, request
from django.views     import View
from reviews.models   import Review
from users.models     import User
from products.models  import Product
from users.utils      import login_decorator

class ReviewView(View):
    def get(self,request, review_id):
        reviews = Review.objects.all()
        result = []

        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse ({"MESSAGE": "REVIEW_DOES_NOT_EXISTS"}, status = 400)   
 
        result = [
            {
                "user"            : review.user.id,
                "product_id"      : review.product_id ,
                "create_at"       : review.created_at,
                "size_rating"     : review.size_rating,
                "color_rating"    : review.color_rating,
                "delivery_rating" : review.delivery_rating,
                "title"           : review.title,
                "comment"         : review.comment,

            } for review in reviews]

        return JsonResponse ({"result": result}, status = 200)

    @login_decorator
    def delete (self,request,review_id):

        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({"MESSAGE": "NO_REVIEWS"}, status = 400)

        if Review.objects.get(id=review_id) != request.user :
            return JsonResponse({"MESSAGE": "UNAUTHROIZED"}, status = 400)

        Review.objects.filter(id=review_id).delete()

        return JsonResponse ({"MESSAGE" : "DELETE"}, status = 204)    

    @login_decorator
    def patch (self,request, review_id):
        try:
            data = json.loads(request.body)

            if not Review.objects.filter(id=review_id).exists():
                return JsonResponse({"MESSAGE": "NO_REVIEWS"}, status = 400)

            if Review.objects.get(id=review_id) != request.user :
                return JsonResponse({"MESSAGE": "UNAUTHROIZED"}, status = 400)

            Review.objects.filter(id= data["review_id"]).update(data["title"], data["comment"])

            return JsonResponse ({"MESSAGE" : "UPDATE"}, status = 200)    

        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"},status = 400)    