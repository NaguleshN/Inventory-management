
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
import sweetify

#User

def home(request):
    products = Product.objects.all()
    query = request.GET.get('query', '')

    if query:
       products = products.filter(name__icontains = query)

    return render(request, 'home.html', {'products': products,})


def about(request):
	return render(request, 'about.html')
 
def logs(request):
	return render(request, 'logs.html')

def cart(request):
	return render(request, 'cart.html')

#Product Details
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
         print("exec add product")
         sweetify.success(request, 'Product added successfully',button="OK")
         return redirect("Add_product")
    
   return render (request,"add_product.html",{"category":category})

def add_category(request):
     categories = Category.objects.all()
     if request.method == "POST":
         name = request.POST.get('name')
         roll_no = request.POST.get('created_by')

         Category.objects.create(name = name,created_by = roll_no)
     return render(request, 'add_category.html', {'categories': categories})

def add_wastage(request):
    categories=Category.objects.all()
    products = Product.objects.all()
    if request.method == "POST":
       product = request.POST.get('product_name')
       product_name = Product.objects.get(name = product) 
       roll_number = request.POST.get('roll_number')
       quantity = request.POST.get('quantity')
       reason = request.POST.get('reason')
       cat=request.POST.get("category")

       category=Category.objects.get(name=cat)

       Wastage.objects.create(product_name=product_name,
                              roll_number=roll_number,
                              quantity=quantity,
                              reason=reason,
                              category=category,
                              )   
    return render(request, 'wastage.html', {'category':categories,
      'products':products,})

def product_description(request, pk):
    item = get_object_or_404(Product, pk =pk)
    return render(request, 'product_description.html', {'item':item,})