from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.TextChoices):
    FOOD = 'food', 'Food & Dining'
    TRANSPORT = 'transport', 'Transport'
    HOUSING = 'housing', 'Housing & Rent'
    UTILITIES = 'utilities', 'Utilities'
    HEALTHCARE = 'healthcare', 'Healthcare'
    ENTERTAINMENT = 'entertainment', 'Entertainment'
    SHOPPING = 'shopping', 'Shopping'
    EDUCATION = 'education', 'Education'
    TRAVEL = 'travel', 'Travel'
    SALARY = 'salary', 'Salary'
    FREELANCE = 'freelance', 'Freelance'
    INVESTMENT = 'investment', 'Investment Returns'
    OTHER = 'other', 'Other'


class TransactionType(models.TextChoices):
    EXPENSE = 'expense', 'Expense'
    INCOME = 'income', 'Income'


class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    title = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.EXPENSE)
    date = models.DateField()
    notes = models.TextField(blank=True)
    receipt_url = models.URLField(blank=True)
    is_recurring = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'type']),
            models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f'{self.user.email} | {self.title} | {self.amount}'


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=30, choices=Category.choices)
    monthly_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'budgets'
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.user.email} | {self.category} | {self.monthly_limit}'