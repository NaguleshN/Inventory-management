
from django.shortcuts import render
from .models import *


def home(request):
    products = Product.objects.all()
    query = request.GET.get('query', '')

    if query:
       products = products.filter(name__icontains = query)

    return render(request, 'home.html', {'products': products,})