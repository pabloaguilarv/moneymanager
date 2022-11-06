from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.views.generic import (
    UpdateView,
    ListView,
    CreateView,
    DeleteView,
    DetailView,
)
from .forms import (
    ExpenseForm,
    SettingsForm,
    StatsForm,
)
from .models import (
    Expense,
    Settings,
    Stats
)
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


def current_month_expenses(request):
    """
    It takes the first object from the Settings model, and uses the start_date and end_date fields to
    filter the Expense model
    
    :param request: The request object
    :return: A list of all expenses for the current month.
    """
    instance = Stats.objects.first()
    form = StatsForm(
        request.POST or None,
        instance=instance
    )

    if request.POST:
        Stats.set_filters_POST(Stats,request)

        if form.is_valid():
            form.save()
            instance = Stats.objects.first()
            form = StatsForm(instance=instance)
    else:
        Stats.set_filters(Stats,instance)

    dates = Settings.objects.first()
    queryset = Expense.objects.all().filter(
        date__gte=dates.start_date,
        date__lte=dates.end_date,
        channel__contains = Stats.channel if Stats.channel != 'all methods' else ''
    ).order_by(
        'date' if Stats.sort == 'ascending' else '-date',
        'id' if Stats.sort == 'ascending' else '-id',
    )

    total = Expense.make_totals(queryset)

    context = {
        'set': queryset,
        'total_spent': total[0],
        'total_refunded': total[1],
        'name': 'Current Month',
        'debt': total[0]-total[1],
        'form': form,
    }
    return render(request, 'manager/all_expenses.html', context)


def all_expenses(request):
    queryset = Expense.objects.all().order_by('date')

    total = Expense.make_totals(queryset)

    context = {
        'set': queryset,
        'total_spent': total[0],
        'total_refunded': total[1],
        'debt': total[0]-total[1],
        'name': 'All Expenses',
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
        instance=instance,
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


class ExpenseUpdateView(UpdateView):
    template_name = 'manager/expense_update.html'
    form_class = ExpenseForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Expense, id=id)


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


def week_stats(request):
    dates = Stats.get_week_range(Stats)
    
    queryset = Expense.objects.all().filter(
        date__gte = dates[0],
        date__lte = dates[1]
    )
    prev_queryset = Expense.objects.all().filter(
        date__gte = dates[2],
        date__lte = dates[3]
    )

    totals = Expense.make_totals(queryset)
    prev_totals = Expense.make_totals(prev_queryset)

    context = {
        'spent': totals[0],
        'to_refund': totals[1],
        'real_debt': totals[0]-totals[1],
        'set': queryset,
        'start_date': dates[0],
        'end_date': dates[1],
        'prev_spent': prev_totals[0],
        'prev_to_refund': prev_totals[1],
        'prev_real_debt': prev_totals[0] - prev_totals[1],
        'prev_set': prev_queryset,
    }

    return render(request, 'manager/stats.html', context)