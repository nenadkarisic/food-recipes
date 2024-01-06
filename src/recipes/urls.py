from django.urls import path, re_path, include
from .views import index, UserViewSet  # UserDetailAPI, RegisterUserAPIView,
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', index, name='index'),
    re_path(r'^', include(router.urls)),
    re_path(r'^auth/', include('dj_rest_auth.urls')),
    # path('get-details', UserDetailAPI.as_view()),
    # path('register', RegisterUserAPIView.as_view()),
]
