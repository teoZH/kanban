from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet,TodoViewSet,NotesViewSet


router = routers.DefaultRouter()
router.register(r'company',CompanyViewSet)
router.register(r'todo',TodoViewSet)
router.register(r'notes',NotesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
