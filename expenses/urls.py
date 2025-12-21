from django.urls import path

from .views import CreateCategoryAPIView

api_prefix = "api/v1"

urlpatterns = [
    path(f'{api_prefix}/create/category/', CreateCategoryAPIView.as_view(), name='create_new_category'),
]
