from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth import authenticate

from applibs.logger import get_logger
from users.serializers import LoginSerializer
from applibs.status import (
    LOGIN_SUCCESSFUL,
    VALID_DATA_NOT_FOUND,
    INVALID_LOGIN_CREDENTIALS
)
from applibs.helper import format_output_success

logger = get_logger(__name__)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Serializer errors: %s", errors)
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        email = serializer_data.get("email")
        password = serializer_data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            logger.error("Error occurred while authenticating user.")
            return Response(INVALID_LOGIN_CREDENTIALS, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        response_data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "header_types": settings.SIMPLE_JWT["AUTH_HEADER_TYPES"],
            "expires_in": int(refresh.lifetime.total_seconds())
        }

        return Response(
            format_output_success(LOGIN_SUCCESSFUL,data=response_data),
            status=status.HTTP_200_OK,
        )
