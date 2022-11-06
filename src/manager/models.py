from django.db import models
from django.urls import reverse
from datetime import (
    date,
    timedelta
)
# Create your models here.

class Expense(models.Model):
    channel = models.CharField(
        max_length=120,
        null=False,
        blank=False
    )
    product = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        default='N/A'
    )
    commerce = models.CharField(
        max_length=120,
        blank=False
    )
    participants = models.CharField(
        max_length=120,
        # blank=True
    )
    amount_spent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0

    )
    is_refunded = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='N/A'
    )
    category = models.CharField(
        max_length=10,
        default='Select',
        null=False,
        blank=True
    )
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('manager:expense-details', kwargs={'id': self.id})
    
    def make_totals(queryset):
        total_spent = 0
        total_refunded = 0

        for expense in queryset:
            total_spent += expense.amount_spent
            total_refunded += expense.refund_amount
            
        return total_spent, total_refunded

class Settings(models.Model):
    start_date = models.DateField()

    end_date = models.DateField()

class Stats(models.Model):
    channel = models.CharField(
        max_length = 120,
        null = True,
        blank = True,
        default='all methods'
    )
    sort = models.CharField(
            max_length=120,
            null=True,
            blank=True,
            default='ascending'
    )
    
    def get_week_range(self):
        current_date = date.today()

        week_days = 6

        week_day = date.weekday(current_date)

        days_to_week_end = week_days - week_day

        week_start = current_date - timedelta(days = week_day)
        week_end = current_date + timedelta(days = days_to_week_end)

        prev_start = week_start - timedelta(days = 7)
        prev_end = week_end - timedelta(days = 7)

        return week_start, week_end, prev_start, prev_end


    def set_filters_POST(self, request):
        self.channel = request.POST.get('channel')
        self.sort = request.POST.get('sort')


    def set_filters(self,instance):
        self.channel = instance.channel
        self.sort = instance.sort