import ulid
from typing import Optional

from django.db import models
from django.conf import settings
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
            logger.error(f"Error creating category: {e}")
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