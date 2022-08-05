from django import template

register = template.Library()

@register.filter('currency')
def currency(value):
    return f'${value:,.1f}'