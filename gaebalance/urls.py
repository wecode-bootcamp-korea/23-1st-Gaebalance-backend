from django.urls import path, include

urlpatterns = [
    path('carts', include('carts.urls')),
]
