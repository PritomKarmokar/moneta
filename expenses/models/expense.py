from django.db import models
from django.conf import settings

from .category import Category
from applibs.logger import get_logger

logger = get_logger(__name__)

class ExpenseManager(models.Manager):
    pass

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