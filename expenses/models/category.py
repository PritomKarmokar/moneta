import ulid
from typing import Optional, List

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import QuerySet
from django.contrib.auth.base_user import AbstractBaseUser

from applibs.logger import get_logger

logger = get_logger(__name__)

class CategoryManager(models.Manager):
    def create_new_category(
            self,
            name: str,
            user: AbstractBaseUser
    ) -> Optional["Category"]:
        try:
            db_object = self.create(name=name, user=user)
            logger.info(f"New Category created successfully for user: {user}")
            return db_object
        except Exception as e:
            logger.error(f"Error creating new category object: {e}")
            return None

    def fetch_all_categories(
            self,
            user: AbstractBaseUser
    ) -> QuerySet["Category"]:
        categories = self.filter(user=user)
        logger.info(f"Fetching all available categories for username '{user.username}'")
        return categories

    def fetch_category(
            self,
            category_id: str,
            user: AbstractBaseUser
    ) -> Optional["Category"]:
        try:
            category = self.get(id=category_id, user=user)
            logger.info(f"Category object fetched successfully for user: {user.username} with id: {category_id}")
            return category
        except Exception as e:
            logger.error(f"Error fetching category object: {e}")
            return None

class Category(models.Model):
    id = models.CharField(max_length=26, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "category"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="unique_category_name_per_user"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ulid.new().__str__()
        super().save(*args, **kwargs)

    @property
    def response_data(self) -> dict:
        return {
            "category_name": self.name,
            "created_by": self.user.username,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @property
    def updated_response_data(self) -> dict:
        return {
            "updated_name": self.name,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def update(self, name: str) -> bool:
        try:
            self.name = name
            self.updated_at = timezone.now()
            self.save()
            return True
        except Exception as e:
            logger.error(f"Error updating category object: {e}")
            return False