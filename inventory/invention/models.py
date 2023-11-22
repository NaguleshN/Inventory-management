from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    actual_qty = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

 
    def __str__(self):
        return self.name
 
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
 
    # def __str__(self):
    #     return f'{self.quantity} x {self.product.name}'
 
class Category(models.Model):
    name=models.CharField(max_length=25)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
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

  # def __str__(self):
  #       return self.product 
