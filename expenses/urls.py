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

urlpatterns = [
    path('create/category/', CreateCategoryAPIView.as_view(), name='create_new_category'),
    path('update/category/<str:category_id>/', UpdateCategoryAPIView.as_view(), name='update_category'),
    path('delete/category/<str:category_id>/', DeleteCategoryAPIView.as_view(), name='delete_category'),
    path('category/list/', CategoryListAPIView.as_view(), name='category_list'),

    path('create/expense/', CreateExpenseAPIView.as_view(), name='create_new_expense'),
    path('update/expense/<str:expense_id>/', UpdateExpenseAPIView.as_view(), name='update_expense'),
    path('delete/expense/<str:expense_id>/', DeleteExpenseAPIView.as_view(), name='delete_expense'),
    path('expense/list/', ExpenseListAPIView.as_view(), name='expense_list'),

]
