from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=10)
    decription=models.CharField(max_length=100)
    actual_count=models.PositiveIntegerField()
    available_count=models.PositiveIntegerField()
    category= models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
 
class Category(models.Model):
    name=models.CharField(max_length=25)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

class Logs(models.Model):
    roll_number=models.CharField(max_length=8)
    name=models.CharField(max_length=25)
    time_logged=models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('checked_in','checked_in'),('checked_out','checked_out')])
    no_of_checks=models.PositiveIntegerField()
    created_by = models.OneToOneField(User, on_delete= models.CASCADE)
    

    class Meta:
        verbose_name_plural = 'Log'

    def __str__(self):
        return self.roll_number
    
    
class Cart(models.Model):
    Roll_number=models.CharField(max_length=8)
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    due_date=models.DateTimeField()

    def __str__(self):
        return self.Roll_number


class Wastage(models.Model):
    roll_number=models.CharField(max_length=8)
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    reason=models.TextField()

    def __str__(self):
        return self.roll_number 