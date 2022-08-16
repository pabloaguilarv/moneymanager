from django.contrib import admin
from django.urls import path, re_path
from .views import (
    ExpenseUpdateView,
    settings_update,
    all_expenses,
    create_expense_view,
    current_month_expenses,
    delete_expense,
    dynamic_view,
    delete_expense,
    week_stats,
    # expense_update
)

app_name='manager'

urlpatterns=[
    path('current_month/', current_month_expenses, name='current-month-expenses'),
    path('<int:id>/', dynamic_view, name='expense-details'),
    path('<int:id>/delete/', delete_expense, name='expense-delete'),
    path('all_expenses/', all_expenses, name='all-expenses'),
    # path('<int:id>/update/', expense_update, name='expense-update'),
    path('<int:id>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('settings/', settings_update, name='settings'),
    path('stats/', week_stats, name='stats'),
]