import typing
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.views.generic import (
    UpdateView
)
from .forms import (
    ExpenseForm,
    SettingsForm
)
from .models import (
    Expense,
    Settings
)
from datetime import date

# Create your views here.

def make_totals(queryset):
    total_spent = 0
    total_refunded = 0
    for expense in queryset:
        total_spent += expense.amount_spent
        total_refunded += expense.refund_amount
    return total_spent, total_refunded


def create_expense_view(request):
    form = ExpenseForm(
        request.POST or None,
    )

    if request.POST:
        if form.is_valid():
            form.save()
            form = ExpenseForm()

    context = {
        'form': form
    }

    return render(request, 'manager/expense_create.html', context)


def current_month_expenses(request):
    dates = Settings.objects.first()
    queryset = Expense.objects.all().filter(
        date__gte=dates.start_date,
        date__lte=dates.end_date
    ).order_by('date')

    total = make_totals(queryset)

    context = {
        'set': queryset,
        'total_spent': total[0],
        'total_refunded': total[1],
        'name': 'Current Month',
        'debt': total[0]-total[1],
    }
    return render(request, 'manager/all_expenses.html', context)


def all_expenses(request):
    queryset = Expense.objects.all().order_by('date')

    total = make_totals(queryset)

    context = {
        'set': queryset,
        'total_spent': total[0],
        'total_refunded': total[1],
        'debt': total[0]-total[1],
        'name': 'All Expenses'
    }
    return render(request, 'manager/all_expenses.html', context)


def dynamic_view(request, id):
    expense = get_object_or_404(Expense, id=id)

    context = {
        'expense': expense
    }
    return render(request, 'manager/expense_details.html', context)


def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.POST:
        expense.delete()
        return redirect('/manager/current_month')
    
    context = {
        'expense': expense
    }
    return render(request, 'manager/expense_delete.html', context)

def expense_update(request, id):
    instance = get_object_or_404(Expense, id=id)
    form = ExpenseForm(
        request.POST or None,
        instance=instance
    )

    if request.POST:
        if form.is_valid():
            form.save()
            form = ExpenseForm()
            return redirect(f'manager/{id}')
    
    context = {
        'form': form,
    }

    return render(request, 'manager/expense_update.html', context)


def settings_update(request):
    instance = Settings.objects.first()
    form = SettingsForm(
        request.POST or None,
        instance=instance
    )

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('/manager/current_month')
    
    context = {
        'form': form
    }

    return render(request, 'manager/settings.html', context)