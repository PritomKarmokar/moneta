from django.contrib import admin

from expenses.models import Expense, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
    )
    search_fields = (
        'user',
        'name'
    )
    list_filter = (
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
    search_fields = (
        'id',
        'user',
        'category',
    )
    list_filter = (
        'user',
        'category',
    )
    orderby = ('user','category')