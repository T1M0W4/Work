from django.shortcuts import render

def catalog(request):
    return render(request, 'vinyls/catalog.html')

def product(request):
    return render(request, 'vinyls/product.html')