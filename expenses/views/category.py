from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from applibs.helper import format_output_success
from applibs.status import (
    NO_CATEGORIES_FOUND,
    VALID_DATA_NOT_FOUND,
    CATEGORY_OBJECT_CREATION_FAILED,
    CATEGORY_LIST_FETCH_SUCCESSFUL,
    NEW_CATEGORY_CREATED_SUCCESSFULLY,
)
from expenses.models import Category
from expenses.serializers import CreateCategorySerializer

logger = get_logger(__name__)

class CreateCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCategorySerializer

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Serializer errors: %s", errors)
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        name = serializer_data.get("name")
        user = request.user
        new_category = Category.objects.create_new_category(name=name, user=user)

        if not new_category:
            logger.error("Error creating new category object.")
            return Response(CATEGORY_OBJECT_CREATION_FAILED, status=status.HTTP_400_BAD_REQUEST)

        return Response(format_output_success(NEW_CATEGORY_CREATED_SUCCESSFULLY, new_category.response_data), status=status.HTTP_201_CREATED)


class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        categories = Category.objects.fetch_all_categories(user=user)
        if len(categories) == 0:
            logger.info("No categories found for user: %s", user.username)
            return Response(format_output_success(NO_CATEGORIES_FOUND), status=status.HTTP_200_OK)

        category_list = []
        for category in categories:
            category_list.append(category.name)

        response_dict = {
            "categories": category_list
        }
        return Response(format_output_success(CATEGORY_LIST_FETCH_SUCCESSFUL, response_dict), status=status.HTTP_200_OK)


