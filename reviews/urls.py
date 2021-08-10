from django.urls   import path
from reviews.views import ReviewPostingView

urlpatterns = [
    path('', ReviewPostingView.as_view()),
]
