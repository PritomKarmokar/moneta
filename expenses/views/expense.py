from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from applibs.helper import format_output_success, render_serializer_error
from applibs.status import (
    VALID_DATA_NOT_FOUND,
    EXPENSE_OBJECT_CREATION_FAILED,
    EXPENSE_OBJECT_CREATED_SUCCESSFULLY
)
from expenses.models import Expense
from expenses.serializers import CreateExpenseSerializer

logger = get_logger(__name__)

class CreateExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateExpenseSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Serializer errors: %s", errors)
            return Response(render_serializer_error(errors), status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        user = request.user
        new_expense = Expense.objects.create_new_expense(payload=serializer_data, user=user)
        if not new_expense:
            logger.error("Error creating new expense object.")
            return Response(EXPENSE_OBJECT_CREATION_FAILED, status=status.HTTP_400_BAD_REQUEST)

        return Response(format_output_success(EXPENSE_OBJECT_CREATED_SUCCESSFULLY, new_expense.response_data) ,status=status.HTTP_201_CREATED)