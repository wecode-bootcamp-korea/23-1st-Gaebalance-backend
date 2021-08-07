import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product, Size

class CartView(View):
    @LoginDecorator
    def delete(self, request):
        cart = request.GET.getlist("id")

        if not Cart.objects.filter(id__in = cart).exists():
            return JsonResponse({"message":"CART_DOES_NOT_EXIST"}, status = 400)

        Cart.objects.filter(id__in = cart).delete()

        return JsonResponse({"message":"DELETED"}, status = 204)