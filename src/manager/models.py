from django.db import models
from django.urls import reverse
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

class Settings(models.Model):
    start_date = models.DateField()

    end_date = models.DateField()
