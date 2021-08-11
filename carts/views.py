import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum, F

from carts.models    import Cart
from users.models    import User
from products.models import Product, Size
from users.utils     import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not Product.objects.filter(id = data["product_id"]).exists():
                return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status = 400)
            
            if not Size.objects.filter(id = data["size_id"]).exists():
                return JsonResponse({"message":"SIZE_DOES_NOT_EXIST"}, status = 400)

            if data["count"] == 0:
                return JsonResponse({"message":"INVALID_COUNT"}, status = 400)

            cart, is_created = Cart.objects.get_or_create(user = request.user, product_id = data["product_id"], size_id = data["size_id"])            
            cart.count += data["count"]
            cart.save()
                
            return JsonResponse({"message":"SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

    @login_decorator
    def get(self, request):            
        carts = Cart.objects.filter(user_id = request.user.id)
        total_price = carts.aggregate(price = Sum(F("count") * F("product__price")))

        response = {
            "cart" : [{
                "cart_id" : cart.id,
                "name"    : cart.product.name,
                "image"   : cart.product.image_url,
                "color"   : cart.product.color.name,
                "size"    : cart.size.name,
                "count"   : cart.count,
                "price"   : int(cart.count * cart.product.price)
            } for cart in carts],
            "total_price" : int(total_price["price"])
        }

        return JsonResponse({"response":response}, status = 200)
