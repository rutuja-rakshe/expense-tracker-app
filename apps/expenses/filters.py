import django_filters
from apps.expenses.models import Expense, Category, TransactionType


class ExpenseFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    category = django_filters.MultipleChoiceFilter(choices=Category.choices)
    type = django_filters.ChoiceFilter(choices=TransactionType.choices)
    is_recurring = django_filters.BooleanFilter()
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Expense
        fields = ['category', 'type', 'is_recurring', 'date_from', 'date_to', 'month', 'year']