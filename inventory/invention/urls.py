from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import return_form, AddWastageView, AddReturnView

urlpatterns = [
    #authentication
    path('login/', views.login ,name="login"), 
    path('signup/', views.signup ,name="Register"), 
    path('complete/azuread-tenant-oauth2/home/', views.home ,name="Home"),
    path('logout/', LogoutView.as_view() , name="logout"),

    #Home-Page-And-navbar-page-For-Users
    path('', views.home ,name="Home"), 
    path('about/', views.about , name="About"),
    path('product_description/<int:pk>', views.product_description, name="Product_description"),


    #Admin-and-superadmin
    path('admin_views/', views.admin_view, name='admin_views'),
    path('add_product/', views.add_product ,name="Add_product"), 
    path('add_category/', views.add_category, name="Add_category"),
    path('wastage_render/', views.wastage, name='wastage_render'),


    #access-denied-page
    path('no_permisson/', views.no_permission, name='no_permission'),
    path('forbidden/', views.custom_forbidden, name='custom_forbidden'),

    #superadmin
    path('users/', views.users_list, name='users_list'),
    path('appoint_admin/<int:user_id>/', views.appoint_admin, name='appoint_admin'),
    path('remove_role/<int:user_id>/', views.remove_role, name='remove_role'),

    #cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/submit/', views.submit_cart, name='submit_cart'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('update_quantity/<int:product_id>/<int:quantity>/', views.update_quantity, name='update_quantity'),

    #Return-form
    path('return_form/', views.return_form, name="return_form"),
    path('return_all/<int:item_id>/', views.return_all, name='return_all'),
    path('add_wastage/<int:item_id>/', AddWastageView.as_view(), name="Add_wastage"),
    path('return/<int:item_id>/', AddReturnView.as_view(), name="return"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
