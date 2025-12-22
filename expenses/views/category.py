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
    CATEGORY_OBJECT_UPDATE_FAILED,
    NEW_CATEGORY_CREATED_SUCCESSFULLY,
    CATEGORY_OBJECT_UPDATED_SUCCESSFULLY,
)
from expenses.models import Category
from expenses.serializers import (
    CreateCategorySerializer,
    UpdateCategorySerializer
)

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


class UpdateCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCategorySerializer

    def patch(self, request: Request, category_id: str) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Serializer errors: %s", errors)
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        new_name = serializer_data.get("name")

        user = request.user
        category_obj = Category.objects.fetch_category(category_id=category_id, user=user)
        if not category_obj:
            logger.error("The following category object with id: %s does not exist for user with username %s.", category_id, user.username)
            return Response(NO_CATEGORIES_FOUND, status=status.HTTP_404_NOT_FOUND)

        is_updated = category_obj.update(name=new_name)
        if not is_updated:
            logger.error("Error updating category object with id: %s for user with username %s.", category_id, user.username)
            return Response(CATEGORY_OBJECT_UPDATE_FAILED, status=status.HTTP_400_BAD_REQUEST)

        return Response(format_output_success(CATEGORY_OBJECT_UPDATED_SUCCESSFULLY, category_obj.updated_response_data), status=status.HTTP_200_OK)

