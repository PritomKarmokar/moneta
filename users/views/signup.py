from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User
from applibs.logger import get_logger
from users.serializers import SignUpSerializer
from applibs.status import (
    USER_PROFILE_CREATED,
    USER_PROFILE_CREATION_FAILED
)
from applibs.helper import format_output_success, render_serializer_error

logger = get_logger(__name__)

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request:Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Serializer errors:", repr(errors))
            return Response(render_serializer_error(errors), status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        user = User.objects.create_user(**serializer_data)

        if not user:
            logger.info("Cannot create a new user profile.")
            return Response(USER_PROFILE_CREATION_FAILED, status=status.HTTP_400_BAD_REQUEST)

        return Response(format_output_success(USER_PROFILE_CREATED, user.profile_response_data), status=status.HTTP_201_CREATED)