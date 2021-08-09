from django.views import View
from django.http  import JsonResponse

from products.models import Product

class ProductView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({"message":"PRODUCT_DOES_NOT_EXIST"}, status=400)

        product = Product.objects.get(id=product_id)

        response = {
            "id"               : product.id,
            "name"             : product.name,
            "price"            : int(product.price),
            "style_code"       : product.style_code,
            "origin"           : product.origin,
            "manufacture_date" : product.manufacture_date,
            "description"      : product.description,
            "image_url"        : product.image_url,
            "image_list"       : [image.image_url for image in product.detailimage_set.all()],
            "color"            : product.color.name,
            "sub_category"     : product.sub_category.sub_category,
            "category"         : product.sub_category.category.category,
        }

        return JsonResponse(response, status=200)