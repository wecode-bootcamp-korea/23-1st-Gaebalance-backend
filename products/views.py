from django.views import View
from django.http  import JsonResponse
from django.db.models import Q

from products.models import Product, ProductOption

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

class ProductListView(View):
    def get(self, request):
        group               = request.GET.get('group', None)
        sub_categories      = request.GET.getlist('sub-category', None)
        colors              = request.GET.getlist('color', None)
        sizes               = request.GET.getlist('size', None)
        price_ranges        = request.GET.getlist('price', None)
        sort_by             = request.GET.get('sort', None)

        group_filter        = Q()
        sub_category_filter = Q()
        color_filter        = Q()
        size_filter         = Q()
        price_range_filter  = Q()

        if group:
            if group == 'men':
                group_filter = Q(group='남자')
            else:
                group_filter = Q(group='여자')

        if sub_categories:
            for sub_category in sub_categories:
                sub_category_filter |= Q(sub_category=sub_category)

        if colors:
            for color in colors:
                color_filter |= Q(color=color)

        if sizes:
            option_filter = Q()
            for size in sizes:
                option_filter |= Q(size=size)

            size_filter = Q(id__in=ProductOption.objects.filter(option_filter).values('product'))

        if price_ranges:
            if '1' in price_ranges:
                price_range_filter |= Q(price__lt=50000)
            if '2' in price_ranges:
                price_range_filter |= Q(price__range=(50000,99999))
            if '3' in price_ranges:
                price_range_filter |= Q(price__range=(100000,149999))
            if '4' in price_ranges:
                price_range_filter |= Q(price__range=(150000,199999))
            if '5' in price_ranges:
                price_range_filter |= Q(price__gte=200000)

        products = Product.objects.filter(
                group_filter&
                sub_category_filter&
                color_filter&
                size_filter&
                price_range_filter
            ).order_by('id')

        if sort_by:
            products = products.order_by(sort_by)

        result = [{
                "id"               : product.id,
                "image_url"        : product.image_url,
                "name"             : product.name,
                "price"            : int(product.price),
                "manufacture_date" : product.manufacture_date,
                "stock"            : sum([size.stock for size in product.productoption_set.all()])
            } for product in products]

        return JsonResponse({"response":result}, status=200)
