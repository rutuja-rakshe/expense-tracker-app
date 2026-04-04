from django.contrib import admin
from apps.expenses.models import Expense, Budget


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'amount', 'category', 'type', 'date', 'is_recurring')
    list_filter = ('type', 'category', 'is_recurring', 'date')
    search_fields = ('user__email', 'title', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date',)
    raw_id_fields = ('user',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'monthly_limit')
    list_filter = ('category',)
    search_fields = ('user__email',)
    raw_id_fields = ('user',)