from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'online_shop/home.html',  {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'online_shop/detail.html', {'product': product})
