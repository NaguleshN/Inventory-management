import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
import sweetify
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .decorators import *
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect


def restrict_user_pipeline(strategy, details, user=None, is_new=False, *args, **kwargs):
    allowed_emails = ['nagulesh.22cs@kct.ac.in','chaaivisva.22cs@kct.ac.in','paramasivan.22mc@kct.ac.in']
    if user and user.email not in allowed_emails:
        return redirect('custom_forbidden')
    return {'details': details, 'user': user, 'is_new': is_new}

def custom_forbidden(request):
    if request.method=="POST":
        return render(request, 'login.html')
    return render(request, 'custom_forbidden.html')

@login_required(login_url= 'login')
@allowed_user(allowed_roles=['student_user','admin'])
def home(request):
    if len(request.user.username)>9:
        user = get_object_or_404(User, id=request.user.id)
        admin_group = Group.objects.get(name='admin') 
        user.groups.add(admin_group)
        # return redirect('admin_views')
    products = Product.objects.all()
    purchased_items = PurchasedItem.objects.filter(user = request.user)
    cart_items = Cart.objects.all()
    query = request.GET.get('query', '')
    if query:
       products = products.filter(name__icontains = query)

    # cart_qty = {item.product_name.id:item.quantity for item in cart_items}

    # for product in products:
    #     if product.id in cart_qty:
    #         product.available_count-= cart_qty[product.id]

    # pur_qty = {item.product.id:item.quantity for item in purchased_items}

    # for product in products:
    #     if product.id in pur_qty:
    #         product.available_count -= pur_qty[product.id]

    return render(request, 'home.html', {'products': products,})


@login_required(login_url='login')
def about(request):
	return render(request, 'about.html')

@login_required(login_url='login')
def logs(request):
	return render(request, 'logs.html')


#Product Details
@allowed_user(allowed_roles=(['admin', 'superadmin']))
@login_required(login_url='login')
def add_product(request):
   category=Category.objects.all()
   if request.method=="POST" and request.FILES.get('image'):
         product_name=request.POST.get("name")
         decription=request.POST.get("description")
         actual_count=request.POST.get("actual")
         available_count=request.POST.get("avail")
         img=request.FILES["image"]   
         cat=request.POST.get("category")
         category=Category.objects.get(name=cat)
         print(actual_count)
         print(available_count)
         if int(actual_count) >= int(available_count):
            print("exec add product")
            Product.objects.create(name=product_name,decription=decription,actual_count=actual_count,available_count=available_count,category=category,image=img)
            sweetify.success(request, 'Look Up the Available Quantity',button="OK")
            return redirect("Add_product")
         else:
             sweetify.warning(request, 'Product added successfully',button="OK")
             return redirect("Add_product")
    
   return render (request,"add_product.html",{"category":category})


@allowed_user(allowed_roles=['admin', 'superadmin'])
@login_required(login_url='login')
def add_category(request):
     categories = Category.objects.all()
     if request.method == "POST":
         name = request.POST.get('name')
         Category.objects.create(name = name, created_by = request.user)
     return render(request, 'add_category.html', {'categories': categories})


@login_required(login_url='login')
def add_wastage(request):
    categories=Category.objects.all()
    products = Product.objects.all()
    if request.method == "POST":
       product = request.POST.get('product_name')
       product_name = Product.objects.get(name = product) 
       roll_number = request.POST.get('roll_number')
       quantity = request.POST.get('quantity')
       reason = request.POST.get('reason')
    #    cat=request.POST.get("category")
       p=Product.objects.filter(name=product_name)
       for i in p:
        category=i.category
    #    category=Category.objects.get(name=cat)
       Wastage.objects.create(product_name=product_name,
                              roll_number=roll_number,
                              quantity=quantity,
                              reason=reason,
                              category=category,
                              )   
    return render(request, 'wastage.html', {'category':categories,
      'products':products,})

@login_required(login_url='login')
def product_description(request, pk):
    # item = get_object_or_404(Product, pk =pk)
    item = Product.objects.get( pk =pk)
    return render(request, 'product_description.html', {'item':item,})

@unauthenticated_user
def login(request):
    if request.user.is_authenticated:
        return redirect('Home')
    
    if request.method=='POST':
        rollno=request.POST.get('rollno')

        pattern = r'^\d{2}[A-Z]{3}\d{3}$'
                    
        if re.match(pattern, rollno):
            password="iqube@kct"
            print(rollno)
            print(password)
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

@unauthenticated_user
def register(request):
    details=User.objects.all()   
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == "POST":
        rollno = request.POST.get('rollno')
        pattern = r'^\d{2}[A-Z]{3}\d{3}$'
                 
        if re.match(pattern, rollno):
            password='iqube@kct'
            print(rollno)
            print(password)
            user = User.objects.create_user(username=rollno,password=password)
            user=auth.authenticate(username=rollno,password=password)
            
            #New user in student_user group
            group = Group.objects.get(name='student_user')
            user.groups.add(group)
            
            if user!=None:
                    auth.login(request,user)
                    sweetify.success(request, 'You are successfully created',button="OK")
                    messages.success(request, f"Account Successfully Created for {rollno}")
                    return redirect('login')
                
    return render(request, 'register.html')

@login_required(login_url='login')
def add_to_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    cart_item ,created= Cart.objects.get_or_create(product_name=product,created_by=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('Home')


@login_required(login_url='login')
def view_cart(request):
    cart_items = Cart.objects.filter(created_by=request.user)
    if request.method=="POST":
        for item in cart_items:
            cart_item = PurchasedItem.objects.create(product=item.product_name,quantity=item.quantity, user=request.user)
            cart_item.quantity =item.quantity
            cart_item.save()
            log_item = Log.objects.create(product = item.product_name, user=request.user, quantity = item.quantity, created_at = datetime.now(), status = 'checked_in')
            Cart.objects.filter(product_name=item.product_name).delete()
        return redirect("Home")

    return render(request,'cart.html',{'cart_items': cart_items,})


@login_required(login_url='login')
def remove_from_cart(request,product_id):
    cart_item = Product.objects.get(id=product_id)
    cart_obj=Cart.objects.get(product_name=cart_item,created_by=request.user)
    cart_obj.quantity -= 1
    cart_obj.save()
    if cart_obj.quantity == 0:
        cart_obj.delete()
    return redirect('view_cart')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'superadmin'])
def admin_view(request):
    log = Log.objects.all()
    return render(request, 'admin.html', {'log':log,})


@allowed_user(allowed_roles=(['admin', 'superadmin']))
@login_required(login_url='login')
def wastage(request):
    wastage = Wastage.objects.all()
    return render(request, 'wastage_render.html', {'wastage': wastage,})

def no_permission(request):
    return render(request, 'no_permission.html')


@allowed_user(allowed_roles=['superadmin'])
def appoint_admin(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        admin_group = Group.objects.get(name='admin') 
        user.groups.add(admin_group)
        return redirect('users_list')
    else:
        pass
    return redirect(request, 'users.html', {'user':user, } )


@login_required(login_url='login')
@allowed_user(allowed_roles=['superadmin'])
def remove_role(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        admin_group = Group.objects.get(name='admin') 
        user.groups.remove(admin_group)
        return redirect('users_list')
    else:
        pass
    return redirect(request, 'users.html', {'user':user, } )


@login_required(login_url='login')
@allowed_user(allowed_roles=['superadmin'])
def users_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})
