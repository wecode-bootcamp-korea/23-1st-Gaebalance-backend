import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product, Size
from users.utils import login_deco

class CartView(View):
    @login_deco
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not Product.objects.filter(id = data["product_id"]).exists():
                return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status = 400)
            
            if not Size.objects.filter(id = data["size_id"]).exists():
                return JsonResponse({"message":"SIZE_DOES_NOT_EXIST"}, status = 400)

            if data["count"] == 0:
                return JsonResponse({"message":"INVALID_COUNT"}, status = 400)

            user     = User.objects.get(id = 5)
            product  = Product.objects.get(id = data["product_id"])
            size     = Size.objects.get(id = data["size_id"])

            cart, is_created = Cart.objects.get_or_create(user = user, product = product, size = size)
            
            if is_created:
                cart.count = 0
            
            cart.count += data["count"]
            cart.save()
                
            return JsonResponse({"message":"CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)