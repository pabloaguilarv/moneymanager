from django.contrib import admin
from django.urls import path, re_path
from .views import (
    settings_update,
    all_expenses,
    create_expense_view,
    current_month_expenses,
    delete_expense,
    dynamic_view,
    delete_expense,
    expense_update
)

app_name='manager'

urlpatterns=[
    path('current_month/', current_month_expenses, name='current-month-expenses'),
    path('<int:id>/', dynamic_view, name='expense-details'),
    path('<int:id>/delete/', delete_expense, name='expense-delete'),
    path('all_expenses/', all_expenses, name='expense-delete'),
    path('<int:id>/update/', expense_update, name='expense-update'),
    path('settings/', settings_update, name='settings'),
]