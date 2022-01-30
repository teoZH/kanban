from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.SignInView.as_view(), name='signIn'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('change-password/',views.CustomPasswordChangeView.as_view(),name='change_pass'),
    path('password-changed/',views.CustomPasswordChangedDone.as_view(),name='password_change_done'),
    path('reset/',views.CustomPasswordReset.as_view(),name='password_reset'),
    path('reset/done/',views.CustomPasswordDone.as_view(),name='reset_done'),
    path('reset/<uidb64>/<token>/',views.CustomPasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('reset/complete/',views.CustomPasswordResetComplete.as_view(),name='password_reset_complete'),
    path('logout/',views.SignOut.as_view(), name='logout')
]
