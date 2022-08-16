from django.db import models
from django.urls import reverse
from datetime import date
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
    def get_week_dates(self):
        weekday = date.weekday(date.today())
        day_date = date.today().day

        max_date_day = 6

        self.week_start = day_date-weekday
        self.week_end = day_date+max_date_day-weekday


    def set_week_dates(self):
        year = date.today().year
        month = date.today().month
        self.week_start = date(year, month, self.week_start)
        self.week_end = date(year, month, self.week_end)

    
