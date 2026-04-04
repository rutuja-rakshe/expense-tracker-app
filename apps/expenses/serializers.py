from rest_framework import serializers
from apps.expenses.models import Expense, Budget


class ExpenseSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Expense
        fields = (
            'id', 'title', 'amount', 'category', 'category_display',
            'type', 'type_display', 'date', 'notes', 'receipt_url',
            'is_recurring', 'tags', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Budget
        fields = ('id', 'category', 'category_display', 'monthly_limit', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        if self.instance is None:
            if Budget.objects.filter(user=user, category=data.get('category')).exists():
                raise serializers.ValidationError({'category': 'Budget for this category already exists.'})
        return data


class CategorySummarySerializer(serializers.Serializer):
    category = serializers.CharField()
    category_display = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    count = serializers.IntegerField()
    percentage = serializers.FloatField()
    budget_limit = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    budget_used_pct = serializers.FloatField(allow_null=True)


class DashboardSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    expense_by_category = CategorySummarySerializer(many=True)
    income_by_category = CategorySummarySerializer(many=True)
    daily_totals = serializers.ListField()