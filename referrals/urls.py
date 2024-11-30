from django.urls import path

from .views import RequestPhoneNumberView, ProfileView, RequestAuthCodeView

urlpatterns = [
    path('request-phone/', RequestPhoneNumberView.as_view(), name='request-phone'),
    path('request_auth_code/', RequestAuthCodeView.as_view(), name='request_auth_code'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
]
