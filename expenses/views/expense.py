from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from applibs.pagination import CustomPagination
from applibs.helper import format_output_success, render_serializer_error
from applibs.status import (
    VALID_DATA_NOT_FOUND,
    NO_EXPENSE_OBJECT_FOUND,
    EXPENSE_OBJECT_UPDATE_FAILED,
    EXPENSE_OBJECT_CREATION_FAILED,
    EXPENSE_OBJECT_CREATED_SUCCESSFULLY,
    EXPENSE_OBJECT_UPDATED_SUCCESSFULLY,
    EXPENSE_LIST_FETCHED_SUCCESSFULLY,
    EXPENSE_OBJECT_DELETED_SUCCESSFULLY
)
from expenses.models import Expense
from expenses.serializers import (
    ExpenseListSerializer,
    CreateExpenseSerializer,
    UpdateExpenseSerializer,
)

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

        return Response(format_output_success(EXPENSE_OBJECT_CREATED_SUCCESSFULLY, new_expense.response_data), status=status.HTTP_201_CREATED)

class UpdateExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateExpenseSerializer

    def patch(self, request: Request, expense_id: str) -> Response:
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

        expense_obj = Expense.objects.fetch_expense(expense_id=expense_id, user=user)
        if not expense_obj:
            logger.error("The following expense object with id: %s does not exist for user with username %s.", expense_id, user.username)
            return Response(NO_EXPENSE_OBJECT_FOUND, status=status.HTTP_404_NOT_FOUND)

        is_updated = expense_obj.update(payload=serializer_data)
        if not is_updated:
            logger.error("Error updating expense object with id: %s for user with username %s.", expense_id, user.username)
            return Response(EXPENSE_OBJECT_UPDATE_FAILED, status=status.HTTP_400_BAD_REQUEST)

        return Response(format_output_success(EXPENSE_OBJECT_UPDATED_SUCCESSFULLY, expense_obj.updated_response_data), status=status.HTTP_200_OK)

class DeleteExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, expense_id: str) -> Response:
        user = request.user
        expense_obj = Expense.objects.fetch_expense(expense_id=expense_id, user=user)
        if not expense_obj:
            logger.error(f"Expense {expense_id} not found for user {user.username}")
            return Response(NO_EXPENSE_OBJECT_FOUND, status=status.HTTP_404_NOT_FOUND)

        expense_obj.delete_object()
        return Response(EXPENSE_OBJECT_DELETED_SUCCESSFULLY, status=status.HTTP_204_NO_CONTENT)

class ExpenseListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseListSerializer
    pagination_class = CustomPagination

    def get(self, request: Request) -> Response:
        user = request.user
        paginator = self.pagination_class()

        queryset = Expense.objects.fetch_all_expenses(user=user)
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        result = paginator.get_paginated_response(serializer.data)

        return Response(
            format_output_success(EXPENSE_LIST_FETCHED_SUCCESSFULLY, result.data),
            status=status.HTTP_200_OK
        )

    # note: in case you the 'ExpenseList Serializer'
    # def get(self, request: Request) -> Response:
    #     user = request.user
    #     paginator = self.pagination_class()
    #
    #     queryset = Expense.objects.fetch_all_expenses(user=user)
    #     page = paginator.paginate_queryset(list(queryset), request)
    #
    #     result = paginator.get_paginated_response(page)
    #
    #     return Response(
    #         format_output_success(EXPENSE_LIST_FETCHED_SUCCESSFULLY, result.data),
    #         status=status.HTTP_200_OK
    #     )