from django.urls import path

from .views import (
    CreateCategoryAPIView,
    CategoryListAPIView
)

api_prefix = "api/v1"

urlpatterns = [
    path(f'{api_prefix}/create/category/', CreateCategoryAPIView.as_view(), name='create_new_category'),
    path(f'{api_prefix}/category/list/', CategoryListAPIView.as_view(), name='category_list'),
]
