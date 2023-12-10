from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from datetime import timezone
import datetime
# from datetime.timezone import tz

class Product(models.Model):
    name=models.CharField(max_length=255)
    decription=models.CharField(max_length=100)
    actual_count=models.PositiveIntegerField()
    available_count=models.PositiveIntegerField()
    dummy_count = models.PositiveIntegerField()
    category= models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images')


    def __str__(self):
        return self.name
 
 
class Category(models.Model):
    name=models.CharField(max_length=25)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
temporary_cart = {} 
class Cart(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    due_date=models.DateTimeField(default=datetime.datetime.now())
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product_name)


class Wastage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name=models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    reason=models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.user) 


class PurchasedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime.datetime.now()) 
    status = models.CharField(max_length=20, choices=[('checked_in','checked_in'),('checked_out','checked_out')])
    
    def _str_(self):
        return str(self.product)

    
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(max_length=20, choices=[('checked_in','checked_in'),('checked_out','checked_out')])
    acting = models.CharField(max_length=20, default="hi")
    def _str_(self):
        return str(self.product)

class CheckedOutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(max_length=20, choices=[('checked_in','checked_in'),('checked_out','checked_out')])

    def _str_(self):
        return str(self.product)
