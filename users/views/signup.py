from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User
from applibs.logger import get_logger
from applibs.status import (
    USER_PROFILE_CREATED,
    VALID_DATA_NOT_FOUND,
    USER_PROFILE_CREATION_FAILED
)
from applibs.helper import format_output_success
from users.serializers import SignUpSerializer

logger = get_logger(__name__)

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request:Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            logger.exception("Serializer errors:",serializer.errors)
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        user = User.objects.create_user(**serializer_data)

        if user:
            logger.info("New User Created Successfully")
            return Response(format_output_success(USER_PROFILE_CREATED, user.profile_response_data))

        return Response(USER_PROFILE_CREATION_FAILED, status=status.HTTP_400_BAD_REQUEST)