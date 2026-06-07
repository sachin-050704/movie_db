from django.urls import path,include
from .views import create_order, verify_payment, AdminRentalViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("rental", AdminRentalViewSet)

urlpatterns = [
    path('create-order/', create_order),
    path('verify-payment/', verify_payment),
    path("admin1/", include(router.urls)),
]