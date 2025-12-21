from django.contrib import admin

from expenses.models import Expense, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
    )
    orderby = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'category',
        'amount',
        'date',
    )

    orderby = ('user',)