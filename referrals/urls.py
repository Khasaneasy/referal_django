from django.urls import path
from .views import RequestPhoneNumberView, RequestAuthCodeView, ProfileView

urlpatterns = [
    path('auth/request-phone/', RequestPhoneNumberView.as_view(), name='request-phone'),
    path('auth/request-auth-code/', RequestAuthCodeView.as_view(), name='request-auth-code'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
