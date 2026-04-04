from django.urls import path
from apps.expenses import views

urlpatterns = [
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('budgets/', views.BudgetListCreateView.as_view(), name='budget-list'),
    path('budgets/<int:pk>/', views.BudgetDetailView.as_view(), name='budget-detail'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]