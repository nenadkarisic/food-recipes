from django.urls import path, re_path, include
from rest_framework import routers

from .views import (
    index,
    UserViewSet,
    RegisterUserAPIView,
    CreateRecipeAPIView,
    CreateRatingAPIView,
    get_recipes,
    get_most_used_ingredients
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', index, name='index'),
    re_path(r'^', include(router.urls)),
    re_path(r'^auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterUserAPIView.as_view()),
    path('recipes/', get_recipes, name='get-recipes'),
    path('recipes/create/', CreateRecipeAPIView.as_view()),
    path('ratings/create/', CreateRatingAPIView.as_view()),
    path('ingredients/most-used/', get_most_used_ingredients, name='get-most-used-ingredients')
]
