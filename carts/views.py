import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product, Size

class CartView(View):
    #@LoginDecorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            if data["count"] == 0:
                return JsonResponse({"message":"INVALID_COUNT"}, status = 400)

            if Cart.objects.filter(user = request.user.id, product = data["product_id"], size = data["size_id"]).exists():
                cart = Cart.objects.get(user = request.user.id, product = data["product_id"], size = data["size_id"])
                Cart.objects.update(
                    count = cart.count + data["count"]
                )
                return JsonResponse({"message":"UPDATED"}, status = 200)
            else:
                Cart.objects.create(
                    user     = User.objects.get(id = request.user.id),
                    product  = Product.objects.get(id = data["product_id"]),
                    size     = Size.objects.get(id = data["size_id"]),
                    count    = data["count"]
                )
                return JsonResponse({"message":"CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        except ValueError:
            return JsonResponse({"message":"VALUE_ERROR"}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status = 400)

        except Size.DoesNotExist:
            return JsonResponse({"message":"SIZE_DOES_NOT_EXIST"}, status = 400)