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
    month = date.today().strftime('%m')
    queryset = Expense.objects.all().filter(date__month=month)

    total = make_totals(queryset)

    context = {
        'set': queryset,
        'total_spent': total[0],
        'total_refunded': total[1],
        'name': 'Current Month'
    }
    return render(request, 'manager/all_expenses.html', context)


def all_expenses(request):
    queryset = Expense.objects.all()

    total = make_totals(queryset)

    context = {
        'set': queryset,
        'total_spent': total[0],
        'total_refunded': total[1],
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


class ExpenseUpdateView(UpdateView):
    template_name = 'manager/expense_update.html'
    form_class = ExpenseForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Expense, id=id)

