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
from django.http import HttpResponseRedirect, JsonResponse
from collections import defaultdict
from django.views import View


#Microsoft-Authentication-View-Only-For-Admin
def restrict_user_pipeline(strategy, details, user=None, is_new=False, *args, **kwargs):
    email=AdminMail.objects.all()
    allowed_emails = ['nagulesh.22cs@kct.ac.in']
    for e in email:
        allowed_emails.append(e.mail)
        
    for i in allowed_emails:
        print(i)
    # group = Group.objects.get(name='admin')
    # user.group.add('admin')
    if user and user.email not in allowed_emails:
        return redirect('custom_forbidden')
    return {'details': details, 'user': user, 'is_new': is_new}

def custom_forbidden(request):
    if request.method=="POST":
        return redirect('login')
    return render(request, 'custom_forbidden.html')


#Login-And-Register
@unauthenticated_user
def login(request):
    if request.user.is_authenticated:
        return redirect('Home')
    
    if request.method=='POST':
        rollno=request.POST.get('rollno')
        password="iqube@kct"
        print(rollno)
        print(password)
        user=auth.authenticate(username=rollno,password=password)
        if user != None:
            auth.login(request,user)
            return redirect('Home')
        else:
            return redirect('Register')
 
    return render(request,'credential/login.html')

@unauthenticated_user
def signup(request):
    details=User.objects.all()   
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == "POST":
        rollno = request.POST.get('rollno')
        password='iqube@kct'
        user = User.objects.create_user(username=rollno,password=password)
        user=auth.authenticate(username=rollno,password=password)           
        #New user in student_user group
        group = Group.objects.get(name='student_user')
        user.groups.add(group)
            
        if user!=None:
            auth.login(request,user)
            sweetify.success(request, 'You are successfully created',button="OK")
            messages.success(request, f"Account Successfully Created for {rollno}")
            return redirect('Home')
                
    return render(request, 'credential/register.html')


#Home-Page
@login_required(login_url= 'login')
@allowed_user(allowed_roles=['student_user','admin', 'superadmin'])
def home(request):
    if len(request.user.username)>9:
        user = get_object_or_404(User, id=request.user.id)
        admin_group = Group.objects.get(name='admin') 
        user.groups.add(admin_group)

    products = Product.objects.all()
    query = request.GET.get('query', '')
    if query:
       products = products.filter(name__icontains = query)
    
    return render(request, 'core/home.html', {'products': products,})


#View-Product-Details-As-View-Details
@login_required(login_url='login')
def product_description(request, pk):
    item = Product.objects.get( pk =pk)
    return render(request, 'core/product_description.html', {'item':item,})


#About-Page
@login_required(login_url='login')
def about(request):
	return render(request, 'core/about.html')


#Access-Denied-Page
def no_permission(request):
    return render(request, 'core/no_permission.html')


#Cart Functionality

#Add-To-Cart
temporary_cart = defaultdict(int)
def add_to_cart(request, product_id):
    products = Product.objects.get(id=product_id)
    if products.available_count == 0:
        messages.info(request, 'There is not Available stock for it.')
    if request.method == "POST":
        quantity = request.POST.get("count")
        if quantity is not None: 
            try:
                quantity_int = int(quantity)
                if quantity_int <= products.available_count and quantity_int != 0:
                    temporary_cart[product_id] += quantity_int
                else:
                    messages.warning(request, "Don't give extra quantity.")
            except ValueError:
                return HttpResponse("Invalid quantity")
        return redirect('Home')


#View-Cart
def view_cart(request):
        cart_items = []
        for product_id, quantity in temporary_cart.items():
            product = Product.objects.get(pk=product_id)
            cart_items.append({'product': product, 'quantity': quantity})
        return render(request, 'cart/cart.html', {'cart_items':cart_items,})


#Remove-Cart
def remove_from_cart(request, product_id):
    if product_id in temporary_cart:
        if temporary_cart[product_id] > 0:
                del temporary_cart[product_id]
    return redirect('view_cart')


#Submit-In-Cart
def submit_cart(request):
    for product_id, quantity in temporary_cart.items():
        product = Product.objects.get(pk=product_id)
        if product.available_count >= quantity:
            product.available_count -= quantity
            product.save()
            PurchasedItem.objects.create(product = product,quantity = quantity, user = request.user, date_added = datetime.now() )
            Log.objects.create(product = product,quantity = quantity, user = request.user, status="checked_in", created_at= datetime.now())
    temporary_cart.clear()
    return redirect("Home")


#Optional-Cart-Quantity
def decrease_quantity(request, product_id):
    if product_id in temporary_cart:
        temporary_cart[product_id] -= 1
        if temporary_cart[product_id] == 0:
            del temporary_cart[product_id]
    return redirect('view_cart')



def increase_quantity(request, product_id):
    if product_id in temporary_cart:
        product = Product.objects.get(pk=product_id)
        if product.available_count > temporary_cart[product_id]:
            temporary_cart[product_id] += 1
    return redirect('view_cart')



def update_quantity(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    if product.available_count >= quantity:
        product.available_count -= quantity
        product.save()
        updated_available_quantity = product.available_count
        return JsonResponse({'success': True, 'updatedAvailableQuantity': updated_available_quantity})
    else:
        return JsonResponse({'success': False})
    


#Return-Form-View
def return_form(request):
    purchased_items = Log.objects.filter(user = request.user) 
    return render(request, 'cart/return_form.html', {'purchased_items':purchased_items,})

#Return-All
def return_all(request, item_id):
    item = get_object_or_404(Log, pk=item_id)
    product = item.product

    item.status = 'checked_in'
    item.save()

    CheckedOutLog.objects.create(product=product,quantity=item.quantity,user=request.user,status="checked_out")
    product.available_count += item.quantity
    product.save()

    item.delete()

    return redirect('return_form')


#Damaged-Form
class AddWastageView(View):
    def get(self, request, item_id):
        categories = Category.objects.all()
        products = Log.objects.all()
        item = get_object_or_404(Log, id=item_id)
        return render(
            request,
            'cart/wastage.html',
            {'categories': categories, 'products': products, 'item': item}
        )

    def post(self, request, item_id):
        categories = Category.objects.all()
        products = Log.objects.all()
        item = get_object_or_404(Log, id=item_id)

        damaged_quantity = request.POST.get("damaged_qty")
        reason = request.POST.get("reason")

        if damaged_quantity is not None and damaged_quantity.isdigit() and int(damaged_quantity) <= item.quantity and int(damaged_quantity) > 0:
            damaged_quantity = int(damaged_quantity)
            item.quantity -= damaged_quantity
           
        
            item.save()

            Wastage.objects.create(user=request.user,product_name=item.product,quantity=damaged_quantity,reason=reason,category=item.product.category)
            if item.quantity == 0:
                item.delete()
                return redirect('return_form')
            if item:
                return redirect('return_form')
            
        else:
            messages.warning(request, 'You have to Look up the quantity')

        return render(
            request,
            'cart/wastage.html',
            {'categories': categories, 'products': products, 'item': item}
        )
        
        
#User-Groups

#Super-Admin-Only-view
@login_required(login_url='login')
@allowed_user(allowed_roles=['superadmin'])
def users_list(request):
    users = User.objects.all()
    admins=AdminMail.objects.all()
    pattern= r"^[a-zA-Z0-9_.]+@(kct\.)+(ac\.)+in$"
    if request.method=="POST":
        email=request.POST.get("email")
        print(email)
        if re.match(pattern,email):
            print("valid")
            for i in admins:
                if email==i.mail:
                    sweetify.warning(request, 'Microsoft mail-id already exists ',button="OK")
                    return render(request, 'superadmin_view/users.html', {'users': users,'admins':admins})
            AdminMail.objects.create(mail=email)


    return render(request, 'superadmin_view/users.html', {'users': users,'admins':admins})


#Super-Admin-Remove-The-Admin-Role
# @login_required(login_url='login')
# @allowed_user(allowed_roles=['superadmin'])
# def remove_role(request, user_id):
#     if request.method == 'POST':
#         user = get_object_or_404(User, id=user_id)
#         admin_group = Group.objects.get(name='admin') 
#         user.groups.remove(admin_group)
#         return redirect('users_list')
#     else:
#         pass
#     return redirect(request, 'superadmin_view/users.html', {'user':user, } )


#Super-Admin-Apoint-Admin
# @allowed_user(allowed_roles=['superadmin'])
# def appoint_admin(request, user_id):
#     if request.method == 'POST':
#         user = get_object_or_404(User, id=user_id)
#         admin_group = Group.objects.get(name='admin') 
#         user.groups.add(admin_group)
#         return redirect('users_list')
#     else:
#         pass
#     return redirect(request, 'super_admin/users.html', {'user':user, } )


#Log-For-Admin-SuperAdmin
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'superadmin'])
def admin_view(request):
    log = Log.objects.all()
    purchased_items = PurchasedItem.objects.all()
    checked_out = CheckedOutLog.objects.all()
    return render(request, 'adminview/admin.html', {'log':log, 'checked_out':checked_out, 'purchased_items': purchased_items,})


#Wastage-Record-View-For-Admin-SuperAdmin
@allowed_user(allowed_roles=(['admin', 'superadmin']))
@login_required(login_url='login')
def wastage(request):
    wastage = Wastage.objects.all()
    return render(request, 'adminview/wastage_render.html', {'wastage': wastage,})


#Add-Product-For-Admin-SuperAdmin
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
            Product.objects.create(name=product_name,decription=decription,actual_count=actual_count,available_count=available_count,category=category,image=img, dummy_count = available_count)
            sweetify.success(request, 'Look Up the Available Quantity',button="OK")
            return redirect("Add_product")
         else:
             sweetify.warning(request, 'Product added successfully',button="OK")
             return redirect("Add_product")
    
   return render (request,"adminview/add_product.html",{"category":category})


#Add-Category-For-Admin-SuperAdmin
@allowed_user(allowed_roles=['admin', 'superadmin'])
@login_required(login_url='login')
def add_category(request):
     categories = Category.objects.all()
     if request.method == "POST":
         name = request.POST.get('name')
         Category.objects.create(name = name, created_by = request.user)
     return render(request, 'adminview/add_category.html', {'categories': categories})


