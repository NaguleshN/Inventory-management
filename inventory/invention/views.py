
from django.shortcuts import render,redirect
from .models import *


def home(request):
    products = Product.objects.all()
    query = request.GET.get('query', '')

    if query:
       products = products.filter(name__icontains = query)

    return render(request, 'home.html', {'products': products,})
 
def add_product(request):
   category=Category.objects.all()
   if request.method=="POST":
         product_name=request.POST.get("name")
         decription=request.POST.get("description")
         actual_count=request.POST.get("actual")
         available_count=request.POST.get("avail")
           
         cat=request.POST.get("category")
         category=Category.objects.get(name=cat)
         Product.objects.create(name=product_name,decription=decription,actual_count=actual_count,available_count=available_count,category=category)
         # return render (request,"add_product.html",{"category":category})
         return redirect("Add_product")
    
   return render (request,"add_product.html",{"category":category})