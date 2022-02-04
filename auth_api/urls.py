from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.api_root, name='auth_api_root'),
    path('login/', views.LoginViewApi.as_view(), name='api-login'),
    path('register/', views.RegisterViewApi.as_view(), name='api-register'),
    path('logout/', views.LogoutView.as_view(), name='api-logout'),
    path('test/', views.HelloView.as_view(), name='api-test'),
    path('info/',include(router.urls),name='api-user-info')
]
