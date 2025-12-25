import ulid
from typing import Optional

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import QuerySet
from django.contrib.auth.base_user import AbstractBaseUser

from .category import Category
from applibs.logger import get_logger

logger = get_logger(__name__)

class ExpenseManager(models.Manager):
    def create_new_expense(
        self,
        payload: dict,
        user: AbstractBaseUser
    ) -> Optional["Expense"]:
        try:
            db_object = self.create(
                user = user,
                category = payload.get("category"),
                amount = payload.get("amount"),
                date = timezone.now(),
                description = payload.get("description")
            )
            logger.info(f"New Expense created successfully for user: {user}")
            return db_object
        except Exception as e:
            logger.error(f"Error creating new expense object: {e}")
            return None

    def fetch_all_expenses(
        self,
        user: AbstractBaseUser
    ) -> QuerySet["Expense"]:
        expenses = self.filter(user=user)
        logger.info(f"Fetching all available expenses for username '{user.username}'")
        return expenses

class Expense(models.Model):
    id = models.CharField(max_length=26, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ExpenseManager()

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        db_table = "expense"

    def __str__(self) -> str:
        return f"{self.id}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ulid.new().__str__()
        super().save(*args, **kwargs)

    @property
    def response_data(self) -> dict:
        return {
            "category": self.category.name,
            "amount": self.amount,
            "created_by": self.user.username,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }