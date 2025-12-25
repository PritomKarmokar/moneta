from django.contrib import admin

from expenses.models import Expense, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
    )

    fields = (
        "id",
        "name",
        "user",
    )

    readonly_fields = ("id",)

    search_fields = (
        "name",
        "user__email",
        "user__username",
    )

    list_filter = (
        "user",
        "name",
    )

    ordering = ("name",)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    fields = (
        "id",
        "user",
        "category",
        "amount",
        "date",
        "description",
        "created_at",
        "updated_at",
    )
    list_display = (
        'id',
        'user',
        'category',
        'amount',
        'date',
        'created_at',
    )
    search_fields = (
        'id',
        'user__username',
        'category__name',
    )
    list_filter = (
        'user',
        'category',
    )
    ordering = (
        'created_at',
        'user',
    )