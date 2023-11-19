
from django.shortcuts import render,redirect
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
          roll_no = request.POST.get('roll_no')

          Category.objects.create(name = name,
                                  roll_no = roll_no
                                  )
     return render(request, 'add_category.html', {'categories': categories,})

