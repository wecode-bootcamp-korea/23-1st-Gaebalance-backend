from django.views import View
from django.http  import JsonResponse

from products.models import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            response = {
                "id" : product.id,
                "name" : product.name,
                "price" : int(product.price),
                "style_code" : product.style_code,
                "origin" : product.origin,
                "manufacture_date" : product.manufacture_date,
                "description" : product.description,
                "image_url" : product.image_url,
                "color" : product.color.name,
                "sub_category" : product.sub_category.sub_category,
                "category" : product.sub_category.category.category,
            }

            return JsonResponse({"response": response}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)