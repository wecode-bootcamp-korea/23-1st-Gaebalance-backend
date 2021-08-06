import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

from carts.models import Cart
from users.models import User
from products.models import Product, Size

class CartView(View):
    # @LoginDecorator
    def get(self, request):
        if not Cart.objects.filter(user_id = request.user.id).exists():
            return JsonResponse({"message":"CART_DOES_NOT_EXIST"}, status = 400)
            
        carts       = Cart.objects.filter(user_id = 2)
        total_price = 0
        response    = []

        for cart in carts:
            response.append({
                "name"  : cart.product.name,
                "image" : cart.product.image_url,
                "color" : cart.product.color.name,
                "size"  : cart.size.name,
                "count" : cart.count,
                "price" : cart.count * cart.product.price
            })
            total_price += cart.count * cart.product.price
            
        response.append({"total_price" : total_price})

        return JsonResponse({"response":response}, status = 200)
