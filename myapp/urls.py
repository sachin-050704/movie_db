from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", AdminUserViewSet)

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('userList/', user_list, name='user_list'),
    path('updateUser/<str:username>', update_user, name='update_user'),
    path('profile/', profile, name='profile'),
    path("check-media/", check_media),
    path("admin1/", include(router.urls)),
]