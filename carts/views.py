import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Sum, F

from carts.models import Cart
from users.models import User
from products.models import Product, Size
from users.utils import login_deco

class CartView(View):
    @login_deco
    def get(self, request):            
        carts = Cart.objects.filter(user_id = 4)
        total_price = carts.aggregate(price = Sum(F("count") * F("product__price")))

        response = [{
            "name"  : cart.product.name,
            "image" : cart.product.image_url,
            "color" : cart.product.color.name,
            "size"  : cart.size.name,
            "count" : cart.count,
            "price" : cart.count * cart.product.price}
            for cart in carts]

        response.append({"total_price" : total_price["price"]})

        return JsonResponse({"response":response}, status = 200)