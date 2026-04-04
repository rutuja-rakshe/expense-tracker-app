import logging
import calendar
from decimal import Decimal
from datetime import date

from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from apps.expenses.models import Expense, Budget, Category, TransactionType
from apps.expenses.serializers import ExpenseSerializer, BudgetSerializer, DashboardSerializer
from apps.expenses.filters import ExpenseFilter

logger = logging.getLogger('apps.expenses')


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ['title', 'notes']
    ordering_fields = ['date', 'amount', 'created_at', 'category']
    ordering = ['-date']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        expense = serializer.save(user=self.request.user)
        logger.info(f'Expense created: id={expense.id} user={self.request.user.email} amount={expense.amount}')


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        logger.info(f'Expense deleted: id={instance.id} user={self.request.user.email}')
        instance.delete()


class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = date.today()
        year = int(request.query_params.get('year', today.year))
        month = int(request.query_params.get('month', today.month))

        qs = Expense.objects.filter(user=request.user, date__year=year, date__month=month)

        totals = qs.aggregate(
            total_income=Sum('amount', filter=Q(type=TransactionType.INCOME)),
            total_expenses=Sum('amount', filter=Q(type=TransactionType.EXPENSE)),
            transaction_count=Count('id'),
        )
        total_income = totals['total_income'] or Decimal('0')
        total_expenses = totals['total_expenses'] or Decimal('0')

        budgets = {b.category: b.monthly_limit for b in Budget.objects.filter(user=request.user)}

        def category_breakdown(type_filter):
            rows = (
                qs.filter(type=type_filter)
                .values('category')
                .annotate(total=Sum('amount'), count=Count('id'))
                .order_by('-total')
            )
            grand_total = sum(r['total'] for r in rows) or Decimal('1')
            result = []
            for r in rows:
                cat = r['category']
                budget_limit = budgets.get(cat)
                budget_used_pct = None
                if budget_limit and type_filter == TransactionType.EXPENSE:
                    budget_used_pct = round(float(r['total'] / budget_limit * 100), 1)
                result.append({
                    'category': cat,
                    'category_display': dict(Category.choices).get(cat, cat),
                    'total': r['total'],
                    'count': r['count'],
                    'percentage': round(float(r['total'] / grand_total * 100), 1),
                    'budget_limit': budget_limit,
                    'budget_used_pct': budget_used_pct,
                })
            return result

        daily = (
            qs.annotate(day=TruncDay('date'))
            .values('day', 'type')
            .annotate(total=Sum('amount'))
            .order_by('day')
        )
        daily_map = {}
        for d in daily:
            key = d['day'].strftime('%Y-%m-%d')
            if key not in daily_map:
                daily_map[key] = {'date': key, 'income': 0, 'expense': 0}
            daily_map[key][d['type']] = float(d['total'])

        _, days_in_month = calendar.monthrange(year, month)
        daily_totals = [
            daily_map.get(f'{year}-{month:02d}-{d:02d}', {'date': f'{year}-{month:02d}-{d:02d}', 'income': 0, 'expense': 0})
            for d in range(1, days_in_month + 1)
        ]

        data = {
            'year': year,
            'month': month,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': total_income - total_expenses,
            'transaction_count': totals['transaction_count'],
            'expense_by_category': category_breakdown(TransactionType.EXPENSE),
            'income_by_category': category_breakdown(TransactionType.INCOME),
            'daily_totals': daily_totals,
        }
        return Response(DashboardSerializer(data).data)