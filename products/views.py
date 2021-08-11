from django.views import View
from django.http  import JsonResponse
from django.db.models import Q, Sum, Max

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

class ProductsView(View):
    def get(self, request):
        group          = request.GET.get('group', None)
        sub_categories = request.GET.getlist('sub-category', None)
        colors         = request.GET.getlist('color', None)
        sizes          = request.GET.getlist('size', None)
        price_ranges   = request.GET.getlist('price',None)
        sort_by        = request.GET.get('sort', None)
        
        filters = Q()

        if group:
            filters &= Q(group=group)

        if sub_categories:
            filters &= Q(sub_category__in=sub_categories)

        if colors:
            filters &= Q(color__in=colors)

        if sizes:
            filters &= Q(productoption__size__in=sizes)

        if price_ranges:
            price_filters = Q()
            range_dict = {
                '1' : (0, 49999),
                '2' : (50000, 99999),
                '3' : (100000, 149999),
                '4' : (150000, 199999),
                '5' : (200000, int(Product.objects.aggregate(Max('price'))['price__max'])),
            }

            for price_range in price_ranges:
                price_filters |= Q(price__range=range_dict.get(price_range, (0,0)))
            
            filters &= price_filters

        sort_key = {
            'low-price'  : 'price',
            'high-price' : '-price',
            'newest'     : '-manufacture_date',
            'bestseller' : 'stock'
        }

        products = Product.objects.annotate(stock=Sum('productoption__stock')).filter(filters).order_by(sort_key.get(sort_by,'id'))

        result = [{
                "id"               : product.id,
                "image_url"        : product.image_url,
                "name"             : product.name,
                "price"            : int(product.price),
                "manufacture_date" : product.manufacture_date,
                "stock"            : product.stock
        } for product in products]

        return JsonResponse({"response":result}, status=200)