from django.db import models

class TransactionTypes(models.TextChoices):
    INCOME = 'INC', 'Income'
    EXPENSE = 'EXP', 'Expense'