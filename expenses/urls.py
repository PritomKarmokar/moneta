from django.urls import path

from .views import (
    UpdateCategoryAPIView,
    CreateCategoryAPIView,
    DeleteCategoryAPIView,
    CategoryListAPIView,
    CreateExpenseAPIView,
    UpdateExpenseAPIView,
    DeleteExpenseAPIView,
    ExpenseListAPIView
)

api_prefix = "api/v1"

urlpatterns = [
    path(f'{api_prefix}/create/category/', CreateCategoryAPIView.as_view(), name='create_new_category'),
    path(f'{api_prefix}/update/category/<str:category_id>/', UpdateCategoryAPIView.as_view(), name='update_category'),
    path(f'{api_prefix}/delete/category/<str:category_id>/', DeleteCategoryAPIView.as_view(), name='delete_category'),
    path(f'{api_prefix}/category/list/', CategoryListAPIView.as_view(), name='category_list'),

    path(f'{api_prefix}/create/expense/', CreateExpenseAPIView.as_view(), name='create_new_expense'),
    path(f'{api_prefix}/update/expense/', UpdateExpenseAPIView.as_view(), name='update_new_expense'),
    path(f'{api_prefix}/delete/expense/', DeleteExpenseAPIView.as_view(), name='delete_new_expense'),
    path(f'{api_prefix}/expense/list/', ExpenseListAPIView.as_view(), name='expense_list'),

]
