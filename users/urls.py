from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SignUpView,
    LoginAPIView,
    LogOutAPIView
)

api_prefix = "api/v1"

urlpatterns = [
    path(f'{api_prefix}/signup/', SignUpView.as_view(), name='signup'),
    path(f'{api_prefix}/login/', LoginAPIView.as_view(), name='login'),
    path(f'{api_prefix}/logout/', LogOutAPIView.as_view(), name='logout'),
    path(f'{api_prefix}/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]