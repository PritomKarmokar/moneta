from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.serializers import LogOutSerializer
from applibs.logger import get_logger
from applibs.status import (
    LOGOUT_SUCCESSFUL,
    VALID_DATA_NOT_FOUND,
    VALID_TOKEN_NOT_PROVIDED,
)

logger = get_logger(__name__)

class LogOutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer

    def post(self,  request: Request) -> Response:
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                errors = serializer.errors
                logger.error("Serializer errors: %s", errors)
                return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

            serializer_data = serializer.validated_data
            refresh_token = serializer_data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info("Token successfully Blacklisted.")
            return Response(LOGOUT_SUCCESSFUL, status=status.HTTP_202_ACCEPTED)

        except TokenError as e:
            logger.error("Token error: %s", repr(e))
            return Response(VALID_TOKEN_NOT_PROVIDED, status=status.HTTP_406_NOT_ACCEPTABLE)
