from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.views.generic import (
    UpdateView
)
from .forms import ExpenseForm
from .models import Expense
from datetime import date

# Create your views here.

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


def expense_update(request, id):
    instance = get_object_or_404(Expense,id=id)
    form = ExpenseForm(
        request.POST or None,
        instance=instance
    )

    print(request, request.POST)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(f'/manager/{id}')
    
    context = {
        'form': form
    }
    
    return render(request, 'manager/expense_update.html', context)


def current_month_expenses(request):
    month = date.today().strftime('%m')
    queryset = Expense.objects.all().filter(date__month=month)

    for expense in queryset:
        expense.amount_spent = f'${expense.amount_spent:,.0f}'

        if expense.refund_amount is not None:
            expense.refund_amount = f'${expense.refund_amount:,.0f}'

    context = {
        'set': queryset
    }
    return render(request, 'manager/all_expenses.html', context)


def all_expenses(request):
    queryset = Expense.objects.all()

    for expense in queryset:
        expense.amount_spent = f'${expense.amount_spent:,.0f}'

        if expense.refund_amount is not None:
            expense.refund_amount = f'${expense.refund_amount:,.0f}'

    context = {
        'set': queryset
    }
    return render(request, 'manager/all_expenses.html', context)


def dynamic_view(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.amount_spent = f'${expense.amount_spent:,.0f}'
    if expense.refund_amount:
        expense.refund_amount = f'${expense.refund_amount:,.0f}'
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


class ExpenseUpdateView(UpdateView):
    template_name = 'manager/expense_update.html'
    form_class = ExpenseForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Expense, id=id)

