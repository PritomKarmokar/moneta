from django.urls import path

from .views import (
    SignUpView,
    LoginAPIView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
]