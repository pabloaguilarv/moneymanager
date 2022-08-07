from django import template

register = template.Library()

@register.filter
def currency(value: float) -> str:
    return f'${value:,.1f}'

@register.filter
def cap(string: str) -> str:
    return string.title()