from django.shortcuts import render,redirect, get_object_or_404
from .models import *
import sweetify
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.generic import View
#User

def home(request):
    products = Product.objects.all()
    cart_items = CartItem.objects.all()
    query = request.GET.get('query', '')

    cart_qty = {item.product_id:item.quantity for item in cart_items}
    if query:
       products = products.filter(name__icontains = query)

    for product in products :
      if product.id in cart_qty:
        product.quantity -= cart_qty[product.id]

    return render(request, 'home.html', {'products': products,})


def about(request):
	return render(request, 'about.html')

def cart(request):
	return render(request, 'cart.html')

def login_page(request):
    if request.method=='POST':
        rollno=request.POST.get('rollno')
        password="iqube@kct"
        hashed_password = make_password(password)
        user=auth.authenticate(username=rollno,password=password)
        auth.login(request,user)
        if user != None:
            return redirect('cart:Home')
        else:
            return redirect('cart:Register')
        
    else:
      return render(request,'login.html')

def register(request):
     details=User.objects.all()
    #  print(u)
     
     if request.method == "POST":
                    print('Van')
                    rollno = request.POST.get('rollno')
                    print('lorry')
                    password='iqube@kct'
                    print('3d printer')
                    hashed_password = make_password(password)
                    data = User.objects.create_user(username=rollno,password=password)
                    data.save()
                    print('hi')
                    for i in details:
                        if i.username==rollno:
                            # print("hello")
                            return redirect("cart:Login")
                    

                    print('4d')
                    return redirect('cart:Login')

     return render(request, 'register.html')


 


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

def view_cart(request, item_id):

    print(item_id)
    cart_items = CartItem.objects.filter(user=request.user)
    print(cart_items)
    for i in cart_items:
      print(i)
      print(i.id)
      # for i in :
      #   print(i.id)
    me=CartItem.objects.filter(id=item_id)
    print(me)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method=="POST":
      print("method")
      for i in cart_items:
          products = Product.objects.all()
          print("sahduhf")
          cart_item, created = PurchasedItems.objects.get_or_create(product=i.product, 
                                                       user=request.user)
          print("print")
          cart_item.quantity =i.quantity
          cart_item.save()
          print("save")
 
    return render(request, 'cart.html',{'cart_items': cart_items, 'total_price': total_price})



# def view_cart(request, item_id):
    
#     cart_items = CartItem.objects.filter(user=request.user)
#     print(cart_items)

#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     if request.method == "POST":
#       print("hii")
#       for i in cart_items:
#         print("hello")
#         if i.user==request.user:
#           print("jfidsjf")
#           products = Product.objects.get(id = product_id)
#           print("sahduhf")
#           cart_item, created = PurchasedItems.objects.get_or_create(product=product, 
                                                      #  user=request.user)
    #       print("print")
    #       cart_item.quantity =i.quantity
    #       cart_item.save()
    #       print("save")
          
 
    # return render(request, 'cart.html',{'cart_items': cart_items, 'total_price': total_price})

# class cart_view(View):
#   def get(self, request, product_id, *args, **Kwargs):
#     cart_items = CartItem.objects.filter(user=request.user)
#     return render(request, 'cart.html', {'cart_items':cart_items,})

#   def post(self, request, item_id, *args, **Kwargs):
#     cart_items = CartItem.objects.filter(user=request.user)

#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     if request.method == "POST":
#       for i in cart_items:

#         if i.user==request.user:

#           cart = CartItem.objects.get(id = item_id)

#           cart_item, created = PurchasedItems.objects.get_or_create(cart=cart, 
#                                                        user=request.user)
#           cart_item.quantity =i.quantity
#           cart_item.save()

 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                       user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    

    return redirect('cart:Home')

    
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:Home')
 


