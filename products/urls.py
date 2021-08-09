from django.urls import path

from products.views import ProductView, ProductListView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('', ProductListView.as_view()),
]