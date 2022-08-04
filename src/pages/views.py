from django.shortcuts import render, redirect

# Create your views here.

def base_view(request, *args, **kwargs):
    return render(request, 'base.html', {})