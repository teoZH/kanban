from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet,TodoViewSet


router = routers.DefaultRouter()
router.register(r'company',CompanyViewSet)
router.register(r'todo',TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
