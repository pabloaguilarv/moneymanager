from email.policy import default
from django import forms
from .models import Expense

class DateInput(forms.DateInput):
    input_type = 'date'

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(
        label='',
        widget=DateInput(
            attrs={
                'placeholder': 'Date',
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )
    channel = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Payment Channel',
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )
    product = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'What was bought',
                'class': 'form-control',
                'style': 'width: 200px; height: 100px;',
            }
        )
    )
    commerce = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Where was it bought',
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
                'placeholder': 'How much was spent',
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )
    refund_amount = forms.DecimalField(
        label='',
        widget = forms.NumberInput(
            attrs={
            'placeholder': 'Amount to receive back',
            'class': 'form-control',
            'style': 'width: 200px;',
            }
        ),
        required=False,
        initial=0
    )
    is_refunded = forms.BooleanField(
        label='Have you been refunded?',
        required=False,
    )


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
            }
        ),
        initial='select'
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