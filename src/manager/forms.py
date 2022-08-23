from django import forms
from .models import (
    Expense,
    Settings,
    Stats,
)
from datetime import date
from moneymanager import settings

class DateInput(forms.DateInput):
    input_type = 'date' 


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(
        label='',
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            },
        ),
    )

    CHANNEL_CHOICES = [
        ('channel', 'Channel'),
        ('credit card', 'Credit Card'),
        ('cash', 'Cash'),
        ('bank transfer', 'Bank Transfer'),
    ]
    channel = forms.CharField(
        label='',
        widget=forms.Select(
            choices=CHANNEL_CHOICES,
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        ),
        initial='channel',
        required=True
    )

    def clean_channel(self):
        channel = self.cleaned_data.get('channel')
        if channel == 'channel':
            raise forms.ValidationError('Select a Channel.')
        return channel
        
    product = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'What',
                'class': 'form-control',
                'style': 'width: 200px; height: 80px;',
            }
        )
    )
    commerce = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Where',
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )
    participants = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'People Involved',
                'rows': 5,
                'cols': 10,
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        ),
        required=False
    )
    amount_spent = forms.DecimalField(
        label='',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'How much',
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )
    refund_amount = forms.DecimalField(
        label='',
        widget = forms.NumberInput(
            attrs={
            'placeholder': 'To receive back',
            'class': 'form-control',
            'style': 'width: 200px;',
            }
        ),
        required=False,
    )

    def clean_refund_amount(self):
        refund_amount = self.cleaned_data.get('refund_amount')
        if refund_amount is None:
            return 0
        return refund_amount

    IS_REFUNDED_CHOICES = [
        ('refunded?', 'Refunded?'),
        ('not yet', 'Not yet'),
        ('n/a', 'N/A'),
        ('refunded', 'Refunded'),
        ('partially', 'Partially'),
    ]

    is_refunded = forms.CharField(
        empty_value='Nothing',
        label='',
        required=False,
        widget=forms.Select(
            choices=IS_REFUNDED_CHOICES,
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;'
            }
        ),
        initial = 'refunded?'
    )

    def clean_is_refunded(self):
        is_refunded = self.cleaned_data.get('is_refunded')
        if is_refunded == 'refunded?':
            return f'n/a'
        return is_refunded

    CATEGORY_CHOICES = [
        ('category', 'Category'),
        ('food', 'Food'),
        ('ocio', 'Ocio'),
        ('duties', 'Duties'),
        ('investment', 'Investment')
    ]

    category = forms.CharField(
        label='',
        widget=forms.Select(
            choices=CATEGORY_CHOICES,
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            },
            
        ),
        initial='category'
    )

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category == 'category':
            raise forms.ValidationError('Select a category.')
        return category


    class Meta:
        model = Expense
        fields = [
            'channel',
            'date',
            'product',
            'commerce',
            'participants',
            'amount_spent',
            'refund_amount',
            'is_refunded',
            'category',
        ]
        widgets = {
            'date': DateInput(),
            'channel': forms.TextInput(
                attrs={
                    'class': 'create-button'
                }
            )
        }


class SettingsForm(forms.ModelForm):
    year = date.today().year
    month = date.today().month
    start_date = forms.DateField(
        label='',
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;'
            },
        ),
        initial=date(year, month, 1)
    )
    end_date = forms.DateField(
        label='',
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;'
            },
        ),
        initial=date(year, month, 28)
    )
    class Meta:
        model = Settings
        fields = [
            'start_date',
            'end_date'
        ]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

class StatsForm(forms.ModelForm):
    CHANNEL_CHOICES = [
        ('all methods', 'All methods'),
        ('credit card', 'Credit Card'),
        ('cash', 'Cash'),
        ('bank transfer', 'Bank Transfer'),
    ]

    channel = forms.CharField(
        label='',
        widget=forms.Select(
            choices = CHANNEL_CHOICES,
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            },
        ),
        initial = 'all',
        required=False,
    )

    SORT_CHOICES = [
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    ]

    sort = forms.CharField(
        label='',
        widget=forms.Select(
            choices=SORT_CHOICES,
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            },
        ),
        initial = 'ascending',
        required=False
    )

    class Meta:
        model = Stats
        fields = [
            'channel',
            'sort'
        ]