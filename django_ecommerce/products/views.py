from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Product

def index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

def show(request, id):
    product = Product.objects.get(pk=id)
    return render(request, 'products/show.html', {'product': product})
