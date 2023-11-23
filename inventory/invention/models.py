from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=255)
    decription=models.CharField(max_length=100)
    actual_count=models.PositiveIntegerField()
    available_count=models.PositiveIntegerField()
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
    

class Logs(models.Model):
    roll_number=models.CharField(max_length=8)
    name=models.CharField(max_length=25)
    time_logged=models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('checked_in','checked_in'),('checked_out','checked_out')])
    no_of_checks=models.PositiveIntegerField()
    

    class Meta:
        verbose_name_plural = 'Log'

    def __str__(self):
        return self.roll_number
    
    
class Cart(models.Model):
    # Roll_number=models.CharField(max_length=8)
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    due_date=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Wastage(models.Model):
    roll_number=models.CharField(max_length=8)
    product_name=models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    reason=models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.roll_number 

class PurchasedItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True) 
    def _str_(self):
        return str(self.product)
    
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('checked_in','checked_in'),('checked_out','checked_out')])

    def _str_(self):
        return str(self.product)