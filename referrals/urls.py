from django.urls import path
from .views import RequestPhoneNumberView, RequestAuthCodeView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('auth/request-phone/', RequestPhoneNumberView.as_view(),
         name='request-phone'),
    path('auth/request-auth-code/', RequestAuthCodeView.as_view(),
         name='request-auth-code'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]
