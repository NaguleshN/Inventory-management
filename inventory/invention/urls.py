from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login ,name="Login"), 
    path('home/', views.home ,name="Home"), 
    path('complete/azuread-tenant-oauth2/home/', views.home ,name="Home"), 
    path('about/', views.about , name="About"),

    path('forbidden/', views.custom_forbidden, name='custom_forbidden'),
    #Product detail
    path('add_product/', views.add_product ,name="Add_product"), 
    path('add_category/', views.add_category, name="Add_category"),
    path('register/', views.register ,name="Register"), 
    path('cart/', views.view_cart, name='view_cart'),
    path('logs/', views.logs, name="logs"),
    path('add_wastage/', views.add_wastage, name="Add_wastage"),
    path('add/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('remove/<int:item_id>', views.remove_from_cart, name="remove_from_cart"),
    path('logout/', LogoutView.as_view() , name="logout"),
    # path('cart/', views.cart, name="cart"),
    path('product_description/<int:pk>', views.product_description, name="Product_description"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
