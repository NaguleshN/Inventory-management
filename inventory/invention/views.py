import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
import sweetify
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseForbidden

from .decorators import unauthenticated_user,allowed_user

def restrict_user_pipeline(strategy, details, user=None, is_new=False, *args, **kwargs):
    allowed_emails = ['nagulesh.22cs@kct.ac.in','chaaivisva.22cs@kct.ac.in']
    if user and user.email not in allowed_emails:
        return redirect('custom_forbidden')
    return {'details': details, 'user': user, 'is_new': is_new}

def custom_forbidden(request):
    if request.method=="POST":
        return render(request, 'login.html')
    return render(request, 'custom_forbidden.html')

@login_required
def home(request):

    products = Product.objects.all()
    purchased_items = PurchasedItem.objects.filter(user = request.user)
    cart_items = Cart.objects.all()
    query = request.GET.get('query', '')

    cart_qty = {item.id:item.quantity for item in cart_items}
    
    if query:
       products = products.filter(name__icontains = query)

    pur_qty = {item.id:item.quantity for item in purchased_items}

    for product in products :
      if product.id in cart_qty:
        product.quantity -= cart_qty[product.id]

      if product.id in pur_qty:
        product.quantity -= pur_qty[product.id]
 

    return render(request, 'home.html', {'products': products,})

@login_required
def about(request):
	return render(request, 'about.html')
@login_required
def logs(request):
	return render(request, 'logs.html')

@login_required
def add_product(request):
   category=Category.objects.all()
   if request.method=="POST":
         product_name=request.POST.get("name")
         decription=request.POST.get("description")
         actual_count=request.POST.get("actual")
         available_count=request.POST.get("avail")
         img=request.FILES["image"]   
         cat=request.POST.get("category")
         category=Category.objects.get(name=cat)
         Product.objects.create(name=product_name,decription=decription,actual_count=actual_count,available_count=available_count,category=category,image=img)
         print("exec add product")
         sweetify.success(request, 'Product added successfully',button="OK")
         return redirect("Add_product")
    
   return render (request,"add_product.html",{"category":category})
@login_required
def add_category(request):
     categories = Category.objects.all()
     if request.method == "POST":
         name = request.POST.get('name')
         roll_no = request.POST.get('created_by')

         Category.objects.create(name = name,created_by = roll_no)
     return render(request, 'add_category.html', {'categories': categories})
@login_required
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
@login_required
def product_description(request, pk):
    # item = get_object_or_404(Product, pk =pk)
    item = Product.objects.get( pk =pk)
    return render(request, 'product_description.html', {'item':item,})

def login(request):
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method=='POST':
        rollno=request.POST.get('rollno')

        pattern = r'^\d{2}[A-Z]{3}\d{3}$'
                    
        if re.match(pattern, rollno):
            password="iqube@kct"
            hashed_password = make_password(password)
            user=auth.authenticate(username=rollno,password=password)
            if user != None:
                auth.login(request,user)
                return redirect('Home')
            else:
                return redirect('Register')
                   
        else:
            messages.warning(request, 'You have to look up the Roll Number.')
            return render(request, 'login.html')  

    return render(request,'login.html')

def register(request):
    details=User.objects.all()     
    if request.method == "POST":
        rollno = request.POST.get('rollno')
        pattern = r'^\d{2}[A-Z]{3}\d{3}$'
                    
        if re.match(pattern, rollno):
            password='iqube@kct'
            hashed_password = make_password(password)
            data = User.objects.create_user(username=rollno,password=password)
            data.save()
            for i in details:
                if i.username==rollno:
                    return redirect("Login")                    
        # return render(request, 'register.html') 

    return render(request, 'register.html')

@login_required
def add_to_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    cart_item ,created= Cart.objects.get_or_create(product_name=product,created_by=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('Home')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(created_by=request.user)
    if request.method=="POST":
        for i in cart_items:
            cart_item, created = PurchasedItems.objects.get_or_create(product=i.product_name,quantity=i.quantity, user=request.user)
            cart_item.quantity =i.quantity
            cart_item.save()
            x = datetime.now()
            log_item = Log.objects.create(product = i.product_name, user=request.user, quantity = i.quantity, created_at = x, status = 'checked_in')
            Cart.objects.filter(product_name=i.product_name).delete()
        return redirect("Home")

    return render(request,'cart.html',{'cart_items': cart_items,})


@login_required
def remove_from_cart(request,item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('Home')

